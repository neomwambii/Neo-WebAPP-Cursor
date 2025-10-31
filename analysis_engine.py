import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from collections import Counter
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
import json
import os

class PowerBallAnalyzer:
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
    
    def get_frequency_analysis(self, game_type="PowerBall"):
        """Analyze frequency of numbers"""
        if self.data.empty:
            return {}
        
        game_data = self.data[self.data['game_type'] == game_type].copy()
        if game_data.empty:
            return {}
        
        # Count main numbers
        all_main_numbers = []
        for numbers_str in game_data['main_numbers']:
            try:
                numbers = eval(numbers_str) if isinstance(numbers_str, str) else numbers_str
                all_main_numbers.extend(numbers)
            except:
                continue
        
        # Count powerballs
        all_powerballs = []
        for pb in game_data['powerball']:
            try:
                all_powerballs.append(int(pb))
            except:
                continue
        
        # Calculate frequencies
        main_counter = Counter(all_main_numbers)
        powerball_counter = Counter(all_powerballs)
        
        # Get frequency data
        main_freq = []
        for num in range(1, 51):
            main_freq.append({
                'number': num,
                'frequency': main_counter.get(num, 0),
                'percentage': (main_counter.get(num, 0) / len(game_data)) * 100
            })
        
        powerball_freq = []
        for num in range(1, 21):
            powerball_freq.append({
                'number': num,
                'frequency': powerball_counter.get(num, 0),
                'percentage': (powerball_counter.get(num, 0) / len(game_data)) * 100
            })
        
        return {
            'main_numbers': main_freq,
            'powerballs': powerball_freq,
            'total_draws': len(game_data),
            'most_frequent_main': main_counter.most_common(10),
            'least_frequent_main': main_counter.most_common()[-10:],
            'most_frequent_powerball': powerball_counter.most_common(10),
            'least_frequent_powerball': powerball_counter.most_common()[-10:]
        }
    
    def get_pattern_analysis(self, game_type="PowerBall"):
        """Analyze patterns in the data"""
        if self.data.empty:
            return {}
        
        game_data = self.data[self.data['game_type'] == game_type].copy()
        if game_data.empty:
            return {}
        
        patterns = {
            'even_odd_distribution': {'even': 0, 'odd': 0},
            'low_high_distribution': {'low': 0, 'high': 0},
            'consecutive_numbers': 0,
            'sum_distribution': [],
            'draw_day_distribution': {},
            'gap_analysis': []
        }
        
        for _, row in game_data.iterrows():
            try:
                numbers = eval(row['main_numbers']) if isinstance(row['main_numbers'], str) else row['main_numbers']
                
                # Even/Odd analysis
                even_count = sum(1 for n in numbers if n % 2 == 0)
                patterns['even_odd_distribution']['even'] += even_count
                patterns['even_odd_distribution']['odd'] += (5 - even_count)
                
                # Low/High analysis (1-25 vs 26-50)
                low_count = sum(1 for n in numbers if n <= 25)
                patterns['low_high_distribution']['low'] += low_count
                patterns['low_high_distribution']['high'] += (5 - low_count)
                
                # Consecutive numbers
                sorted_nums = sorted(numbers)
                consecutive = sum(1 for i in range(len(sorted_nums)-1) if sorted_nums[i+1] - sorted_nums[i] == 1)
                patterns['consecutive_numbers'] += consecutive
                
                # Sum analysis
                patterns['sum_distribution'].append(sum(numbers))
                
                # Draw day analysis
                draw_day = row['draw_day']
                patterns['draw_day_distribution'][draw_day] = patterns['draw_day_distribution'].get(draw_day, 0) + 1
                
                # Gap analysis
                gaps = [sorted_nums[i+1] - sorted_nums[i] for i in range(len(sorted_nums)-1)]
                patterns['gap_analysis'].extend(gaps)
                
            except:
                continue
        
        # Calculate statistics
        patterns['even_odd_ratio'] = patterns['even_odd_distribution']['even'] / (patterns['even_odd_distribution']['even'] + patterns['even_odd_distribution']['odd'])
        patterns['low_high_ratio'] = patterns['low_high_distribution']['low'] / (patterns['low_high_distribution']['low'] + patterns['low_high_distribution']['high'])
        patterns['avg_consecutive'] = patterns['consecutive_numbers'] / len(game_data)
        patterns['sum_stats'] = {
            'mean': np.mean(patterns['sum_distribution']),
            'std': np.std(patterns['sum_distribution']),
            'min': np.min(patterns['sum_distribution']),
            'max': np.max(patterns['sum_distribution'])
        }
        patterns['gap_stats'] = {
            'mean': np.mean(patterns['gap_analysis']),
            'std': np.std(patterns['gap_analysis']),
            'min': np.min(patterns['gap_analysis']),
            'max': np.max(patterns['gap_analysis'])
        }
        
        return patterns
    
    def get_trend_analysis(self, game_type="PowerBall", days=30):
        """Analyze recent trends"""
        if self.data.empty:
            return {}
        
        game_data = self.data[self.data['game_type'] == game_type].copy()
        if game_data.empty:
            return {}
        
        # Get recent data
        cutoff_date = datetime.now() - timedelta(days=days)
        recent_data = game_data[game_data['draw_date'] >= cutoff_date]
        
        if recent_data.empty:
            return {}
        
        # Analyze recent patterns
        recent_numbers = []
        for numbers_str in recent_data['main_numbers']:
            try:
                numbers = eval(numbers_str) if isinstance(numbers_str, str) else numbers_str
                recent_numbers.extend(numbers)
            except:
                continue
        
        recent_counter = Counter(recent_numbers)
        
        # Hot numbers (frequent in recent period)
        hot_numbers = recent_counter.most_common(10)
        
        # Cold numbers (infrequent in recent period)
        all_numbers = list(range(1, 51))
        cold_numbers = [(num, recent_counter.get(num, 0)) for num in all_numbers if recent_counter.get(num, 0) <= 1]
        cold_numbers.sort(key=lambda x: x[1])
        cold_numbers = cold_numbers[:10]
        
        return {
            'period_days': days,
            'total_draws': len(recent_data),
            'hot_numbers': hot_numbers,
            'cold_numbers': cold_numbers,
            'trend_direction': self._calculate_trend_direction(recent_data)
        }
    
    def get_draw_day_analysis(self, game_type="PowerBall"):
        """Analyze patterns by draw day"""
        if self.data.empty:
            return {}
        
        game_data = self.data[self.data['game_type'] == game_type].copy()
        if game_data.empty:
            return {}
        
        day_analysis = {}
        
        for day in ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']:
            day_data = game_data[game_data['draw_day'] == day]
            if day_data.empty:
                continue
            
            # Analyze numbers for this day
            day_numbers = []
            for numbers_str in day_data['main_numbers']:
                try:
                    numbers = eval(numbers_str) if isinstance(numbers_str, str) else numbers_str
                    day_numbers.extend(numbers)
                except:
                    continue
            
            day_counter = Counter(day_numbers)
            
            day_analysis[day] = {
                'total_draws': len(day_data),
                'most_frequent': day_counter.most_common(5),
                'least_frequent': day_counter.most_common()[-5:],
                'avg_sum': np.mean([sum(eval(numbers_str) if isinstance(numbers_str, str) else numbers_str) for numbers_str in day_data['main_numbers']])
            }
        
        return day_analysis
    
    def get_analysis(self, analysis_type="frequency"):
        """Get analysis based on type"""
        if analysis_type == "frequency":
            return self.get_frequency_analysis()
        elif analysis_type == "pattern":
            return self.get_pattern_analysis()
        elif analysis_type == "trend":
            return self.get_trend_analysis()
        elif analysis_type == "draw_day":
            return self.get_draw_day_analysis()
        else:
            return {}
    
    def get_draw_history(self, limit=50):
        """Get recent draw history"""
        if self.data.empty:
            return []
        
        # Get recent draws
        recent_data = self.data.head(limit)
        
        history = []
        for _, row in recent_data.iterrows():
            try:
                numbers = eval(row['main_numbers']) if isinstance(row['main_numbers'], str) else row['main_numbers']
                history.append({
                    'draw_date': row['draw_date'].strftime('%Y-%m-%d'),
                    'main_numbers': numbers,
                    'powerball': int(row['powerball']),
                    'game_type': row['game_type'],
                    'draw_day': row['draw_day']
                })
            except:
                continue
        
        return history
    
    def _calculate_trend_direction(self, data):
        """Calculate if numbers are trending up or down"""
        try:
            # Calculate average sum over time
            sums = []
            for numbers_str in data['main_numbers']:
                try:
                    numbers = eval(numbers_str) if isinstance(numbers_str, str) else numbers_str
                    sums.append(sum(numbers))
                except:
                    continue
            
            if len(sums) < 2:
                return "insufficient_data"
            
            # Simple linear trend
            x = np.arange(len(sums))
            y = np.array(sums)
            
            # Calculate slope
            slope = np.polyfit(x, y, 1)[0]
            
            if slope > 1:
                return "increasing"
            elif slope < -1:
                return "decreasing"
            else:
                return "stable"
                
        except:
            return "unknown"
    
    def create_frequency_chart(self, game_type="PowerBall"):
        """Create frequency visualization"""
        freq_data = self.get_frequency_analysis(game_type)
        if not freq_data:
            return None
        
        # Create subplot
        fig = make_subplots(
            rows=2, cols=1,
            subplot_titles=('Main Numbers Frequency', 'PowerBall Frequency'),
            vertical_spacing=0.1
        )
        
        # Main numbers chart
        main_nums = [item['number'] for item in freq_data['main_numbers']]
        main_freqs = [item['frequency'] for item in freq_data['main_numbers']]
        
        fig.add_trace(
            go.Bar(x=main_nums, y=main_freqs, name='Main Numbers'),
            row=1, col=1
        )
        
        # PowerBall chart
        pb_nums = [item['number'] for item in freq_data['powerballs']]
        pb_freqs = [item['frequency'] for item in freq_data['powerballs']]
        
        fig.add_trace(
            go.Bar(x=pb_nums, y=pb_freqs, name='PowerBall'),
            row=2, col=1
        )
        
        fig.update_layout(
            title=f'Number Frequency Analysis - {game_type}',
            height=800,
            showlegend=False
        )
        
        return fig.to_json()
    
    def create_pattern_chart(self, game_type="PowerBall"):
        """Create pattern visualization"""
        pattern_data = self.get_pattern_analysis(game_type)
        if not pattern_data:
            return None
        
        # Create subplots
        fig = make_subplots(
            rows=2, cols=2,
            subplot_titles=('Even/Odd Distribution', 'Low/High Distribution', 
                          'Sum Distribution', 'Gap Analysis'),
            specs=[[{"type": "pie"}, {"type": "pie"}],
                   [{"type": "histogram"}, {"type": "histogram"}]]
        )
        
        # Even/Odd pie chart
        even_odd_data = pattern_data['even_odd_distribution']
        fig.add_trace(
            go.Pie(labels=['Even', 'Odd'], values=[even_odd_data['even'], even_odd_data['odd']]),
            row=1, col=1
        )
        
        # Low/High pie chart
        low_high_data = pattern_data['low_high_distribution']
        fig.add_trace(
            go.Pie(labels=['Low (1-25)', 'High (26-50)'], values=[low_high_data['low'], low_high_data['high']]),
            row=1, col=2
        )
        
        # Sum distribution
        fig.add_trace(
            go.Histogram(x=pattern_data['sum_distribution'], name='Sum Distribution'),
            row=2, col=1
        )
        
        # Gap analysis
        fig.add_trace(
            go.Histogram(x=pattern_data['gap_analysis'], name='Gap Analysis'),
            row=2, col=2
        )
        
        fig.update_layout(
            title=f'Pattern Analysis - {game_type}',
            height=800,
            showlegend=False
        )
        
        return fig.to_json()

if __name__ == "__main__":
    analyzer = PowerBallAnalyzer()
    
    # Test frequency analysis
    freq_analysis = analyzer.get_frequency_analysis()
    print("Frequency Analysis:")
    print(f"Most frequent main numbers: {freq_analysis.get('most_frequent_main', [])[:5]}")
    print(f"Most frequent powerballs: {freq_analysis.get('most_frequent_powerball', [])[:5]}")
    
    # Test pattern analysis
    pattern_analysis = analyzer.get_pattern_analysis()
    print(f"\nPattern Analysis:")
    print(f"Even/Odd ratio: {pattern_analysis.get('even_odd_ratio', 0):.2f}")
    print(f"Low/High ratio: {pattern_analysis.get('low_high_ratio', 0):.2f}")
    print(f"Average consecutive: {pattern_analysis.get('avg_consecutive', 0):.2f}")
