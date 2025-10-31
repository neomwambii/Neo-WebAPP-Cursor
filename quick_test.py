#!/usr/bin/env python3

import sys
import os

# Add current directory to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def test_system():
    """Quick test of the PowerBall prediction system"""
    print("🎯 PowerBall Prediction System - Quick Test")
    print("=" * 50)
    
    try:
        # Test 1: Create sample data
        print("1. Creating sample data...")
        from simple_data_collector import SimplePowerBallCollector
        collector = SimplePowerBallCollector()
        data = collector.collect_data()
        print(f"   ✅ Created {len(data)} sample draws")
        
        # Test 2: Test prediction engine
        print("\n2. Testing prediction engine...")
        from prediction_engine import PowerBallPredictor
        predictor = PowerBallPredictor()
        
        strategies = ['frequency', 'cold_numbers', 'pattern', 'balanced']
        for strategy in strategies:
            try:
                predictions = predictor.get_predictions(strategy)
                print(f"   ✅ {strategy}: {len(predictions)} predictions generated")
                if predictions:
                    pred = predictions[0]
                    print(f"      Sample: {pred['main_numbers']} + {pred['powerball']}")
            except Exception as e:
                print(f"   ❌ {strategy}: {e}")
        
        # Test 3: Test analysis engine
        print("\n3. Testing analysis engine...")
        from analysis_engine import PowerBallAnalyzer
        analyzer = PowerBallAnalyzer()
        
        try:
            freq_analysis = analyzer.get_frequency_analysis()
            print(f"   ✅ Frequency analysis: {freq_analysis.get('total_draws', 0)} draws analyzed")
        except Exception as e:
            print(f"   ❌ Analysis error: {e}")
        
        # Test 4: Check data files
        print("\n4. Checking data files...")
        data_files = [
            "data/powerball_data.csv",
            "data/powerball_plus_data.csv",
            "data/all_powerball_data.csv"
        ]
        
        for file_path in data_files:
            if os.path.exists(file_path):
                size = os.path.getsize(file_path)
                print(f"   ✅ {file_path} ({size} bytes)")
            else:
                print(f"   ❌ {file_path} (not found)")
        
        print("\n" + "=" * 50)
        print("🎉 System Test Complete!")
        print("\nTo start the web application:")
        print("  C:\\Python313\\python.exe app.py")
        print("\nThen open: http://localhost:5000")
        
        return True
        
    except ImportError as e:
        print(f"❌ Import error: {e}")
        print("Please install required packages:")
        print("  C:\\Python313\\python.exe -m pip install -r requirements.txt")
        return False
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    test_system()

