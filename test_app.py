#!/usr/bin/env python3

import sys
import os

# Add current directory to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

try:
    from simple_data_collector import SimplePowerBallCollector
    print("✓ Simple data collector imported successfully")
    
    collector = SimplePowerBallCollector()
    print("✓ Collector initialized")
    
    data = collector.collect_data()
    print(f"✓ Data collection completed. Total draws: {len(data)}")
    
    # Check if data files were created
    if os.path.exists("data/powerball_data.csv"):
        print("✓ PowerBall data file created")
    else:
        print("✗ PowerBall data file not found")
    
    if os.path.exists("data/powerball_plus_data.csv"):
        print("✓ PowerBall Plus data file created")
    else:
        print("✗ PowerBall Plus data file not found")
    
    if os.path.exists("data/all_powerball_data.csv"):
        print("✓ Combined data file created")
    else:
        print("✗ Combined data file not found")
        
except ImportError as e:
    print(f"✗ Import error: {e}")
except Exception as e:
    print(f"✗ Error: {e}")
    import traceback
    traceback.print_exc()

