#!/usr/bin/env python3

import sys
import os
import json
from datetime import datetime

# Add current directory to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def demo_predictions():
    """Demonstrate prediction capabilities"""
    print("🎯 PowerBall Prediction Demo")
    print("=" * 50)
    
    try:
        from prediction_engine import PowerBallPredictor
        from analysis_engine import PowerBallAnalyzer
        
        # Initialize components
        predictor = PowerBallPredictor()
        analyzer = PowerBallAnalyzer()
        
        print("✓ Components initialized")
        
        # Show available strategies
        strategies = ['frequency', 'cold_numbers', 'pattern', 'machine_learning', 'balanced']
        
        for strategy in strategies:
            print(f"\n📊 {strategy.replace('_', ' ').title()} Strategy:")
            print("-" * 30)
            
            try:
                predictions = predictor.get_predictions(strategy)
                
                for i, pred in enumerate(predictions[:3], 1):  # Show first 3 predictions
                    main_nums = pred['main_numbers']
                    powerball = pred['powerball']
                    confidence = pred['confidence']
                    
                    print(f"  Prediction {i}: {main_nums} + {powerball} (Confidence: {confidence:.2f})")
                    
            except Exception as e:
                print(f"  Error: {e}")
        
        # Show analysis
        print(f"\n📈 Analysis Demo:")
        print("-" * 30)
        
        try:
            freq_analysis = analyzer.get_frequency_analysis()
            if freq_analysis:
                print(f"Total draws analyzed: {freq_analysis.get('total_draws', 0)}")
                
                most_frequent = freq_analysis.get('most_frequent_main', [])[:5]
                if most_frequent:
                    print(f"Most frequent numbers: {[item[0] for item in most_frequent]}")
                
                least_frequent = freq_analysis.get('least_frequent_main', [])[:5]
                if least_frequent:
                    print(f"Least frequent numbers: {[item[0] for item in least_frequent]}")
            
            pattern_analysis = analyzer.get_pattern_analysis()
            if pattern_analysis:
                print(f"Even/Odd ratio: {pattern_analysis.get('even_odd_ratio', 0):.2f}")
                print(f"Low/High ratio: {pattern_analysis.get('low_high_ratio', 0):.2f}")
                print(f"Average consecutive: {pattern_analysis.get('avg_consecutive', 0):.2f}")
                
        except Exception as e:
            print(f"Analysis error: {e}")
        
        print(f"\n✅ Demo completed successfully!")
        print(f"🌐 To use the web interface, run: python app.py")
        print(f"📱 Then open: http://localhost:5000")
        
    except ImportError as e:
        print(f"❌ Import error: {e}")
        print("Please run setup.py first to install dependencies")
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()

def check_data():
    """Check if data files exist"""
    print("📁 Checking data files...")
    
    data_files = [
        "data/powerball_data.csv",
        "data/powerball_plus_data.csv", 
        "data/all_powerball_data.csv"
    ]
    
    for file_path in data_files:
        if os.path.exists(file_path):
            size = os.path.getsize(file_path)
            print(f"✓ {file_path} ({size} bytes)")
        else:
            print(f"✗ {file_path} (not found)")
    
    print()

if __name__ == "__main__":
    print("🎲 South African PowerBall Predictor Demo")
    print("=" * 50)
    print()
    
    check_data()
    demo_predictions()

