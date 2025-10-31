import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import random
from collections import Counter
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
import warnings
import os
warnings.filterwarnings('ignore')

class PowerBallPredictor:
    def __init__(self, data_file="data/all_powerball_data.csv"):
        self.data_file = data_file
        self.data = None
        self.load_data()
        
    def load_data(self):
        """Load historical data"""
        try:
            if os.path.exists(self.data_file):
                df = pd.read_csv(self.data_file)
                df['draw_date'] = pd.to_datetime(df['draw_date'])
                self.data = df
            else:
                print(f"Data file {self.data_file} not found. Please run data collection first.")
                self.data = pd.DataFrame()
        except Exception as e:
            print(f"Error loading data: {e}")
            self.data = pd.DataFrame()
    
    def get_frequency_predictions(self, game_type="PowerBall", top_n=10):
        """Predict based on most frequently drawn numbers"""
        if self.data.empty:
            return self._get_random_predictions()
        
        # Filter by game type
        game_data = self.data[self.data['game_type'] == game_type].copy()
        if game_data.empty:
            return self._get_random_predictions()
        
        # Count frequency of main numbers
        all_main_numbers = []
        for numbers_str in game_data['main_numbers']:
            try:
                # Parse the string representation of list
                numbers = eval(numbers_str) if isinstance(numbers_str, str) else numbers_str
                all_main_numbers.extend(numbers)
            except:
                continue
        
        # Count frequency of powerballs
        all_powerballs = []
        for pb in game_data['powerball']:
            try:
                all_powerballs.append(int(pb))
            except:
                continue
        
        # Get most frequent numbers
        main_counter = Counter(all_main_numbers)
        powerball_counter = Counter(all_powerballs)
        
        # Get top numbers for main numbers (1-50)
        top_main = [num for num, count in main_counter.most_common() if 1 <= num <= 50][:top_n]
        
        # Get top numbers for powerball (1-20)
        top_powerball = [num for num, count in powerball_counter.most_common() if 1 <= num <= 20][:top_n]
        
        # Generate predictions
        predictions = []
        for i in range(5):  # Generate 5 different combinations
            # Select 5 unique main numbers from top frequent
            main_nums = random.sample(top_main, min(5, len(top_main)))
            if len(main_nums) < 5:
                # Fill with random numbers if not enough frequent numbers
                remaining = [n for n in range(1, 51) if n not in main_nums]
                main_nums.extend(random.sample(remaining, 5 - len(main_nums)))
            
            main_nums = sorted(main_nums[:5])
            
            # Select powerball from top frequent
            powerball = random.choice(top_powerball) if top_powerball else random.randint(1, 20)
            
            predictions.append({
                'main_numbers': main_nums,
                'powerball': powerball,
                'strategy': 'frequency',
                'confidence': self._calculate_confidence(main_nums, powerball, main_counter, powerball_counter)
            })
        
        return predictions
    
    def get_cold_numbers_predictions(self, game_type="PowerBall", top_n=10):
        """Predict based on least frequently drawn numbers (cold numbers)"""
        if self.data.empty:
            return self._get_random_predictions()
        
        game_data = self.data[self.data['game_type'] == game_type].copy()
        if game_data.empty:
            return self._get_random_predictions()
        
        # Count frequency of all numbers
        all_main_numbers = []
        for numbers_str in game_data['main_numbers']:
            try:
                numbers = eval(numbers_str) if isinstance(numbers_str, str) else numbers_str
                all_main_numbers.extend(numbers)
            except:
                continue
        
        all_powerballs = []
        for pb in game_data['powerball']:
            try:
                all_powerballs.append(int(pb))
            except:
                continue
        
        # Get least frequent numbers
        main_counter = Counter(all_main_numbers)
        powerball_counter = Counter(all_powerballs)
        
        # Get cold numbers (least frequent)
        all_main_nums = list(range(1, 51))
        cold_main = [num for num in all_main_nums if num not in main_counter or main_counter[num] == 0]
        cold_main.extend([num for num, count in main_counter.most_common()[-top_n:] if num not in cold_main])
        
        all_powerball_nums = list(range(1, 21))
        cold_powerball = [num for num in all_powerball_nums if num not in powerball_counter or powerball_counter[num] == 0]
        cold_powerball.extend([num for num, count in powerball_counter.most_common()[-top_n:] if num not in cold_powerball])
        
        # Generate predictions
        predictions = []
        for i in range(5):
            main_nums = random.sample(cold_main, min(5, len(cold_main)))
            if len(main_nums) < 5:
                remaining = [n for n in range(1, 51) if n not in main_nums]
                main_nums.extend(random.sample(remaining, 5 - len(main_nums)))
            
            main_nums = sorted(main_nums[:5])
            powerball = random.choice(cold_powerball) if cold_powerball else random.randint(1, 20)
            
            predictions.append({
                'main_numbers': main_nums,
                'powerball': powerball,
                'strategy': 'cold_numbers',
                'confidence': self._calculate_confidence(main_nums, powerball, main_counter, powerball_counter)
            })
        
        return predictions
    
    def get_pattern_predictions(self, game_type="PowerBall"):
        """Predict based on number patterns and sequences"""
        if self.data.empty:
            return self._get_random_predictions()
        
        game_data = self.data[self.data['game_type'] == game_type].copy()
        if game_data.empty:
            return self._get_random_predictions()
        
        # Analyze patterns
        patterns = self._analyze_patterns(game_data)
        
        predictions = []
        for i in range(5):
            # Generate based on patterns
            main_nums = self._generate_pattern_based_numbers(patterns)
            powerball = random.randint(1, 20)  # Powerball is less predictable
            
            predictions.append({
                'main_numbers': main_nums,
                'powerball': powerball,
                'strategy': 'pattern_analysis',
                'confidence': 0.6  # Medium confidence for pattern-based
            })
        
        return predictions
    
    def get_ml_predictions(self, game_type="PowerBall"):
        """Predict using machine learning approach"""
        if self.data.empty or len(self.data) < 100:
            return self._get_random_predictions()
        
        try:
            game_data = self.data[self.data['game_type'] == game_type].copy()
            if game_data.empty:
                return self._get_random_predictions()
            
            # Prepare features
            features = self._prepare_ml_features(game_data)
            if features is None or len(features) < 50:
                return self._get_random_predictions()
            
            # Train models for each number position
            predictions = []
            
            for i in range(5):  # 5 main numbers
                model = RandomForestClassifier(n_estimators=100, random_state=42)
                
                # Prepare target (next number in position i)
                X = features[:-1]  # All but last
                y = []
                
                for j in range(len(game_data) - 1):
                    try:
                        numbers = eval(game_data.iloc[j+1]['main_numbers']) if isinstance(game_data.iloc[j+1]['main_numbers'], str) else game_data.iloc[j+1]['main_numbers']
                        y.append(numbers[i] if i < len(numbers) else random.randint(1, 50))
                    except:
                        y.append(random.randint(1, 50))
                
                if len(X) != len(y):
                    continue
                
                # Train model
                model.fit(X, y)
                
                # Predict next number
                next_features = features[-1].reshape(1, -1)
                predicted_number = model.predict(next_features)[0]
                
                # Ensure number is in valid range
                predicted_number = max(1, min(50, predicted_number))
                
                predictions.append(predicted_number)
            
            # Generate 5 different combinations
            final_predictions = []
            for i in range(5):
                main_nums = sorted(random.sample(predictions, min(5, len(predictions))))
                if len(main_nums) < 5:
                    remaining = [n for n in range(1, 51) if n not in main_nums]
                    main_nums.extend(random.sample(remaining, 5 - len(main_nums)))
                
                main_nums = sorted(main_nums[:5])
                powerball = random.randint(1, 20)
                
                final_predictions.append({
                    'main_numbers': main_nums,
                    'powerball': powerball,
                    'strategy': 'machine_learning',
                    'confidence': 0.7
                })
            
            return final_predictions
            
        except Exception as e:
            print(f"ML prediction error: {e}")
            return self._get_random_predictions()
    
    def get_balanced_predictions(self, game_type="PowerBall"):
        """Combine multiple strategies for balanced predictions"""
        if self.data.empty:
            return self._get_random_predictions()
        
        # Get predictions from different strategies
        freq_preds = self.get_frequency_predictions(game_type, top_n=15)
        cold_preds = self.get_cold_numbers_predictions(game_type, top_n=15)
        pattern_preds = self.get_pattern_predictions(game_type)
        
        # Combine and balance
        all_predictions = freq_preds + cold_preds + pattern_preds
        
        # Select diverse predictions
        selected = []
        used_combinations = set()
        
        for pred in all_predictions:
            combo = tuple(pred['main_numbers'])
            if combo not in used_combinations:
                selected.append(pred)
                used_combinations.add(combo)
                if len(selected) >= 5:
                    break
        
        return selected[:5]
    
    def get_predictions(self, strategy="frequency", game_type="PowerBall"):
        """Get predictions based on specified strategy"""
        if strategy == "frequency":
            return self.get_frequency_predictions(game_type)
        elif strategy == "cold_numbers":
            return self.get_cold_numbers_predictions(game_type)
        elif strategy == "pattern":
            return self.get_pattern_predictions(game_type)
        elif strategy == "machine_learning":
            return self.get_ml_predictions(game_type)
        elif strategy == "balanced":
            return self.get_balanced_predictions(game_type)
        else:
            return self._get_random_predictions()
    
    def _get_random_predictions(self):
        """Generate random predictions as fallback"""
        predictions = []
        for i in range(5):
            main_nums = sorted(random.sample(range(1, 51), 5))
            powerball = random.randint(1, 20)
            predictions.append({
                'main_numbers': main_nums,
                'powerball': powerball,
                'strategy': 'random',
                'confidence': 0.1
            })
        return predictions
    
    def _calculate_confidence(self, main_nums, powerball, main_counter, powerball_counter):
        """Calculate confidence score for predictions"""
        try:
            # Calculate average frequency of selected numbers
            main_freq = sum(main_counter.get(num, 0) for num in main_nums) / len(main_nums)
            powerball_freq = powerball_counter.get(powerball, 0)
            
            # Normalize confidence (0-1 scale)
            max_main_freq = max(main_counter.values()) if main_counter else 1
            max_powerball_freq = max(powerball_counter.values()) if powerball_counter else 1
            
            confidence = (main_freq / max_main_freq + powerball_freq / max_powerball_freq) / 2
            return min(1.0, max(0.1, confidence))
        except:
            return 0.5
    
    def _analyze_patterns(self, data):
        """Analyze number patterns in historical data"""
        patterns = {
            'even_odd_ratio': [],
            'low_high_ratio': [],
            'consecutive_numbers': [],
            'sum_ranges': []
        }
        
        for _, row in data.iterrows():
            try:
                numbers = eval(row['main_numbers']) if isinstance(row['main_numbers'], str) else row['main_numbers']
                
                # Even/Odd ratio
                even_count = sum(1 for n in numbers if n % 2 == 0)
                patterns['even_odd_ratio'].append(even_count / len(numbers))
                
                # Low/High ratio (1-25 vs 26-50)
                low_count = sum(1 for n in numbers if n <= 25)
                patterns['low_high_ratio'].append(low_count / len(numbers))
                
                # Consecutive numbers
                consecutive = sum(1 for i in range(len(numbers)-1) if numbers[i+1] - numbers[i] == 1)
                patterns['consecutive_numbers'].append(consecutive)
                
                # Sum range
                patterns['sum_ranges'].append(sum(numbers))
                
            except:
                continue
        
        return patterns
    
    def _generate_pattern_based_numbers(self, patterns):
        """Generate numbers based on analyzed patterns"""
        # Use average patterns to guide selection
        avg_even_ratio = np.mean(patterns['even_odd_ratio']) if patterns['even_odd_ratio'] else 0.5
        avg_low_ratio = np.mean(patterns['low_high_ratio']) if patterns['low_high_ratio'] else 0.5
        
        numbers = []
        
        # Select numbers based on even/odd ratio
        even_needed = int(5 * avg_even_ratio)
        odd_needed = 5 - even_needed
        
        # Even numbers
        even_nums = [n for n in range(2, 51, 2)]
        numbers.extend(random.sample(even_nums, min(even_needed, len(even_nums))))
        
        # Odd numbers
        odd_nums = [n for n in range(1, 51, 2)]
        numbers.extend(random.sample(odd_nums, min(odd_needed, len(odd_nums))))
        
        # Fill remaining slots
        while len(numbers) < 5:
            remaining = [n for n in range(1, 51) if n not in numbers]
            if remaining:
                numbers.append(random.choice(remaining))
            else:
                break
        
        return sorted(numbers[:5])
    
    def _prepare_ml_features(self, data):
        """Prepare features for machine learning"""
        try:
            features = []
            
            for i in range(len(data) - 1):
                feature_row = []
                
                # Previous draw numbers
                try:
                    prev_numbers = eval(data.iloc[i]['main_numbers']) if isinstance(data.iloc[i]['main_numbers'], str) else data.iloc[i]['main_numbers']
                    feature_row.extend(prev_numbers)
                except:
                    feature_row.extend([0] * 5)
                
                # Draw day of week (encoded)
                draw_date = pd.to_datetime(data.iloc[i]['draw_date'])
                feature_row.append(draw_date.weekday())
                
                # Time since last draw
                if i > 0:
                    prev_date = pd.to_datetime(data.iloc[i-1]['draw_date'])
                    days_diff = (draw_date - prev_date).days
                    feature_row.append(days_diff)
                else:
                    feature_row.append(7)  # Default weekly
                
                # Rolling averages
                if i >= 5:
                    recent_numbers = []
                    for j in range(i-5, i):
                        try:
                            nums = eval(data.iloc[j]['main_numbers']) if isinstance(data.iloc[j]['main_numbers'], str) else data.iloc[j]['main_numbers']
                            recent_numbers.extend(nums)
                        except:
                            continue
                    
                    if recent_numbers:
                        feature_row.append(np.mean(recent_numbers))
                        feature_row.append(np.std(recent_numbers))
                    else:
                        feature_row.extend([25, 15])  # Defaults
                else:
                    feature_row.extend([25, 15])  # Defaults
                
                features.append(feature_row)
            
            return np.array(features)
            
        except Exception as e:
            print(f"Feature preparation error: {e}")
            return None

if __name__ == "__main__":
    predictor = PowerBallPredictor()
    predictions = predictor.get_predictions("balanced")
    for i, pred in enumerate(predictions, 1):
        print(f"Prediction {i}: {pred['main_numbers']} + {pred['powerball']} (Confidence: {pred['confidence']:.2f})")
