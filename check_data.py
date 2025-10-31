#!/usr/bin/env python3

import pandas as pd
import os

def check_data():
    print("📊 Current Data Analysis")
    print("=" * 30)
    
    # Check if data files exist
    data_files = [
        'data/powerball_data.csv',
        'data/powerball_plus_data.csv', 
        'data/all_powerball_data.csv'
    ]
    
    for file_path in data_files:
        if os.path.exists(file_path):
            size = os.path.getsize(file_path)
            print(f"✅ {file_path} ({size:,} bytes)")
        else:
            print(f"❌ {file_path} (not found)")
    
    # Analyze the main data file
    if os.path.exists('data/all_powerball_data.csv'):
        print(f"\n📈 Data Analysis:")
        df = pd.read_csv('data/all_powerball_data.csv')
        
        print(f"Total draws: {len(df):,}")
        print(f"Date range: {df['draw_date'].min()} to {df['draw_date'].max()}")
        print(f"Game types: {df['game_type'].value_counts().to_dict()}")
        
        print(f"\n📋 Sample draws:")
        for i, row in df.head(3).iterrows():
            print(f"  {i+1}. {row['draw_date']} - {row['main_numbers']} + {row['powerball']} ({row['game_type']})")
        
        # Check if this is sample data
        print(f"\n🔍 Data Source Analysis:")
        
        # Look for indicators of sample data
        if 'raw_text' in df.columns:
            print("❌ This is SAMPLE DATA (contains 'raw_text' column)")
        elif len(df) > 1000:
            print("⚠️  Large dataset - could be sample or real data")
        else:
            print("🤔 Data source unclear")
        
        # Check for realistic patterns
        all_numbers = []
        for numbers_str in df['main_numbers']:
            try:
                numbers = eval(numbers_str) if isinstance(numbers_str, str) else numbers_str
                all_numbers.extend(numbers)
            except:
                pass
        
        if all_numbers:
            from collections import Counter
            counter = Counter(all_numbers)
            most_common = counter.most_common(5)
            print(f"Most frequent numbers: {[item[0] for item in most_common]}")
            
            # Check if distribution looks realistic
            if len(set(all_numbers)) > 40:  # Good distribution
                print("✅ Number distribution looks realistic")
            else:
                print("⚠️  Number distribution may be limited")

if __name__ == "__main__":
    check_data()

