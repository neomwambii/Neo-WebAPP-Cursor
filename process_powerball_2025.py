#!/usr/bin/env python3

import pandas as pd
from datetime import datetime
import os

def process_powerball_2025_data():
    """Process the PowerBall 2025 data from screenshots"""
    
    # PowerBall 2025 data extracted from screenshots
    powerball_2025_data = [
        # October 2025
        {"draw_date": "2025-10-14", "main_numbers": [5, 25, 31, 40, 41], "powerball": 20, "jackpot": 140432581.79, "outcome": "Roll"},
        {"draw_date": "2025-10-10", "main_numbers": [6, 10, 40, 44, 50], "powerball": 11, "jackpot": 130599836.88, "outcome": "Roll"},
        {"draw_date": "2025-10-07", "main_numbers": [13, 18, 21, 23, 24], "powerball": 16, "jackpot": 120535458.29, "outcome": "Roll"},
        {"draw_date": "2025-10-03", "main_numbers": [12, 14, 33, 41, 44], "powerball": 10, "jackpot": 111052301.71, "outcome": "Roll"},
        {"draw_date": "2025-09-30", "main_numbers": [14, 22, 25, 37, 46], "powerball": 4, "jackpot": 101389351.24, "outcome": "Roll"},
        {"draw_date": "2025-09-26", "main_numbers": [3, 13, 19, 24, 40], "powerball": 12, "jackpot": 92151099.05, "outcome": "Roll"},
        {"draw_date": "2025-09-23", "main_numbers": [10, 23, 32, 43, 45], "powerball": 18, "jackpot": 84371860.00, "outcome": "Roll"},
        {"draw_date": "2025-09-19", "main_numbers": [2, 16, 24, 41, 47], "powerball": 19, "jackpot": 77327031.76, "outcome": "Roll"},
        {"draw_date": "2025-09-16", "main_numbers": [22, 24, 26, 33, 35], "powerball": 7, "jackpot": 70421371.73, "outcome": "Roll"},
        {"draw_date": "2025-09-12", "main_numbers": [17, 23, 25, 26, 37], "powerball": 18, "jackpot": 64157390.24, "outcome": "Roll"},
        {"draw_date": "2025-09-09", "main_numbers": [21, 28, 40, 43, 45], "powerball": 13, "jackpot": 57196404.35, "outcome": "Roll"},
        {"draw_date": "2025-09-05", "main_numbers": [22, 30, 33, 35, 38], "powerball": 20, "jackpot": 51027875.26, "outcome": "Roll"},
        {"draw_date": "2025-09-02", "main_numbers": [20, 31, 33, 34, 50], "powerball": 6, "jackpot": 44169356.63, "outcome": "Roll"},
        {"draw_date": "2025-08-29", "main_numbers": [12, 14, 29, 45, 50], "powerball": 15, "jackpot": 37954435.45, "outcome": "Roll"},
        {"draw_date": "2025-08-26", "main_numbers": [13, 19, 24, 44, 50], "powerball": 15, "jackpot": 31588677.88, "outcome": "Roll"},
        {"draw_date": "2025-08-22", "main_numbers": [4, 10, 27, 37, 50], "powerball": 18, "jackpot": 26244913.07, "outcome": "Roll"},
        
        # August 2025 (continued)
        {"draw_date": "2025-08-19", "main_numbers": [2, 10, 22, 27, 40], "powerball": 17, "jackpot": 20801659.73, "outcome": "Roll"},
        {"draw_date": "2025-08-15", "main_numbers": [4, 11, 19, 32, 33], "powerball": 12, "jackpot": 15906361.60, "outcome": "Roll"},
        {"draw_date": "2025-08-12", "main_numbers": [8, 10, 20, 41, 48], "powerball": 4, "jackpot": 10474598.91, "outcome": "Roll"},
        {"draw_date": "2025-08-08", "main_numbers": [13, 26, 39, 41, 48], "powerball": 18, "jackpot": 5732993.11, "outcome": "Roll"},
        {"draw_date": "2025-08-05", "main_numbers": [10, 32, 34, 40, 48], "powerball": 14, "jackpot": 124602697.30, "outcome": "Won"},
        {"draw_date": "2025-08-01", "main_numbers": [5, 31, 33, 34, 40], "powerball": 13, "jackpot": 113570848.93, "outcome": "Roll"},
        {"draw_date": "2025-07-29", "main_numbers": [4, 17, 20, 24, 30], "powerball": 19, "jackpot": 102978317.76, "outcome": "Roll"},
        {"draw_date": "2025-07-25", "main_numbers": [3, 29, 35, 39, 42], "powerball": 5, "jackpot": 93497143.60, "outcome": "Roll"},
        {"draw_date": "2025-07-22", "main_numbers": [3, 8, 10, 27, 49], "powerball": 1, "jackpot": 84823734.90, "outcome": "Roll"},
        {"draw_date": "2025-07-18", "main_numbers": [10, 15, 26, 31, 41], "powerball": 5, "jackpot": 78124219.01, "outcome": "Roll"},
        {"draw_date": "2025-07-15", "main_numbers": [5, 21, 26, 28, 39], "powerball": 6, "jackpot": 71174882.63, "outcome": "Roll"},
        {"draw_date": "2025-07-11", "main_numbers": [1, 7, 8, 15, 20], "powerball": 15, "jackpot": 65000000.00, "outcome": "Roll"},
        {"draw_date": "2025-07-08", "main_numbers": [14, 19, 37, 44, 48], "powerball": 17, "jackpot": 56728199.73, "outcome": "Roll"},
        {"draw_date": "2025-07-04", "main_numbers": [15, 16, 22, 30, 32], "powerball": 7, "jackpot": 51334513.69, "outcome": "Roll"},
        {"draw_date": "2025-07-01", "main_numbers": [8, 9, 26, 30, 31], "powerball": 8, "jackpot": 45797029.17, "outcome": "Roll"},
        
        # June 2025
        {"draw_date": "2025-06-27", "main_numbers": [11, 23, 32, 41, 47], "powerball": 17, "jackpot": 41395254.14, "outcome": "Roll"},
        {"draw_date": "2025-06-24", "main_numbers": [2, 22, 27, 36, 39], "powerball": 19, "jackpot": 32454283.04, "outcome": "Roll"},
        {"draw_date": "2025-06-20", "main_numbers": [22, 23, 25, 29, 42], "powerball": 8, "jackpot": 32454283.04, "outcome": "Roll"},
        {"draw_date": "2025-06-17", "main_numbers": [5, 23, 26, 38, 43], "powerball": 4, "jackpot": 27759453.39, "outcome": "Roll"},
        {"draw_date": "2025-06-13", "main_numbers": [1, 21, 34, 46, 47], "powerball": 12, "jackpot": 24278118.55, "outcome": "Roll"},
        {"draw_date": "2025-06-10", "main_numbers": [5, 11, 23, 29, 48], "powerball": 1, "jackpot": 20002422.86, "outcome": "Roll"},
        {"draw_date": "2025-06-06", "main_numbers": [9, 24, 34, 41, 44], "powerball": 2, "jackpot": 16193925.27, "outcome": "Roll"},
        {"draw_date": "2025-06-03", "main_numbers": [5, 26, 40, 47, 50], "powerball": 14, "jackpot": 12127002.75, "outcome": "Roll"},
        {"draw_date": "2025-05-30", "main_numbers": [10, 13, 34, 43, 46], "powerball": 1, "jackpot": 9038632.35, "outcome": "Roll"},
        {"draw_date": "2025-05-27", "main_numbers": [13, 22, 33, 38, 50], "powerball": 15, "jackpot": 4122336.47, "outcome": "Roll"},
        {"draw_date": "2025-05-23", "main_numbers": [1, 17, 18, 27, 49], "powerball": 15, "jackpot": 68123803.20, "outcome": "Won"},
        {"draw_date": "2025-05-20", "main_numbers": [13, 26, 31, 32, 47], "powerball": 18, "jackpot": 61517481.68, "outcome": "Roll"},
        {"draw_date": "2025-05-16", "main_numbers": [9, 16, 20, 28, 39], "powerball": 19, "jackpot": 56153697.45, "outcome": "Roll"},
        {"draw_date": "2025-05-13", "main_numbers": [11, 21, 29, 37, 39], "powerball": 12, "jackpot": 50493786.94, "outcome": "Roll"},
        {"draw_date": "2025-05-09", "main_numbers": [5, 6, 14, 38, 50], "powerball": 10, "jackpot": 45262605.34, "outcome": "Roll"},
        {"draw_date": "2025-05-06", "main_numbers": [19, 20, 32, 35, 37], "powerball": 19, "jackpot": 39478388.27, "outcome": "Roll"},
        {"draw_date": "2025-05-02", "main_numbers": [2, 6, 17, 37, 47], "powerball": 9, "jackpot": 33781651.48, "outcome": "Roll"},
        
        # April 2025
        {"draw_date": "2025-04-29", "main_numbers": [5, 14, 32, 33, 45], "powerball": 13, "jackpot": 27984968.95, "outcome": "Roll"},
        {"draw_date": "2025-04-25", "main_numbers": [5, 9, 13, 46, 47], "powerball": 11, "jackpot": 23223991.19, "outcome": "Roll"},
        {"draw_date": "2025-04-22", "main_numbers": [18, 32, 33, 38, 43], "powerball": 9, "jackpot": 17880242.37, "outcome": "Roll"},
        {"draw_date": "2025-04-18", "main_numbers": [15, 17, 22, 33, 45], "powerball": 12, "jackpot": 13990312.34, "outcome": "Roll"},
        {"draw_date": "2025-04-15", "main_numbers": [19, 24, 38, 40, 41], "powerball": 2, "jackpot": 9828704.13, "outcome": "Roll"},
        {"draw_date": "2025-04-11", "main_numbers": [5, 12, 14, 22, 48], "powerball": 18, "jackpot": 5157546.54, "outcome": "Roll"},
        {"draw_date": "2025-04-08", "main_numbers": [1, 16, 23, 37, 42], "powerball": 6, "jackpot": 110904086.10, "outcome": "Won"},
        {"draw_date": "2025-04-04", "main_numbers": [8, 20, 35, 36, 38], "powerball": 2, "jackpot": 101298652.87, "outcome": "Roll"},
        {"draw_date": "2025-04-01", "main_numbers": [1, 6, 12, 13, 36], "powerball": 7, "jackpot": 90347329.49, "outcome": "Roll"},
        {"draw_date": "2025-03-28", "main_numbers": [1, 6, 13, 14, 35], "powerball": 3, "jackpot": 82421422.17, "outcome": "Roll"},
        {"draw_date": "2025-03-25", "main_numbers": [22, 32, 38, 39, 40], "powerball": 10, "jackpot": 73647329.74, "outcome": "Roll"},
        {"draw_date": "2025-03-21", "main_numbers": [9, 16, 24, 32, 50], "powerball": 19, "jackpot": 67000000.00, "outcome": "Roll"},
        {"draw_date": "2025-03-18", "main_numbers": [15, 22, 29, 35, 43], "powerball": 10, "jackpot": 57800318.05, "outcome": "Roll"},
        {"draw_date": "2025-03-14", "main_numbers": [7, 32, 38, 45, 46], "powerball": 2, "jackpot": 52000000.00, "outcome": "Roll"},
        {"draw_date": "2025-03-11", "main_numbers": [8, 28, 30, 44, 48], "powerball": 2, "jackpot": 42592219.27, "outcome": "Roll"},
        {"draw_date": "2025-03-07", "main_numbers": [12, 13, 16, 28, 46], "powerball": 3, "jackpot": 36856449.42, "outcome": "Roll"},
        {"draw_date": "2025-03-04", "main_numbers": [20, 23, 35, 43, 50], "powerball": 15, "jackpot": 30683508.62, "outcome": "Roll"},
        
        # February 2025
        {"draw_date": "2025-02-28", "main_numbers": [11, 19, 20, 21, 44], "powerball": 6, "jackpot": 24958675.04, "outcome": "Roll"},
        {"draw_date": "2025-02-25", "main_numbers": [18, 23, 27, 34, 44], "powerball": 18, "jackpot": 18820734.27, "outcome": "Roll"},
        {"draw_date": "2025-02-21", "main_numbers": [2, 3, 15, 17, 42], "powerball": 5, "jackpot": 13975244.77, "outcome": "Roll"},
        {"draw_date": "2025-02-18", "main_numbers": [16, 19, 34, 36, 43], "powerball": 16, "jackpot": 9110248.22, "outcome": "Roll"},
        {"draw_date": "2025-02-14", "main_numbers": [2, 8, 25, 37, 44], "powerball": 18, "jackpot": 4806831.46, "outcome": "Roll"},
        {"draw_date": "2025-02-11", "main_numbers": [7, 15, 21, 23, 33], "powerball": 13, "jackpot": 4124764.70, "outcome": "Won"},
        {"draw_date": "2025-02-07", "main_numbers": [7, 30, 34, 42, 49], "powerball": 1, "jackpot": 19927387.50, "outcome": "Won"},
        {"draw_date": "2025-02-04", "main_numbers": [19, 23, 27, 41, 49], "powerball": 8, "jackpot": 14360025.40, "outcome": "Roll"},
        {"draw_date": "2025-01-31", "main_numbers": [3, 27, 36, 40, 47], "powerball": 15, "jackpot": 9690015.75, "outcome": "Roll"},
        {"draw_date": "2025-01-28", "main_numbers": [17, 21, 26, 42, 43], "powerball": 14, "jackpot": 4460619.37, "outcome": "Roll"},
        {"draw_date": "2025-01-24", "main_numbers": [12, 15, 24, 43, 49], "powerball": 18, "jackpot": 102670563.40, "outcome": "Won"},
        {"draw_date": "2025-01-21", "main_numbers": [1, 2, 15, 23, 37], "powerball": 4, "jackpot": 93412308.12, "outcome": "Roll"},
        {"draw_date": "2025-01-17", "main_numbers": [4, 11, 27, 39, 40], "powerball": 8, "jackpot": 86522804.80, "outcome": "Roll"},
        {"draw_date": "2025-01-14", "main_numbers": [20, 23, 30, 34, 44], "powerball": 7, "jackpot": 79095543.13, "outcome": "Roll"},
        {"draw_date": "2025-01-10", "main_numbers": [10, 14, 33, 44, 47], "powerball": 2, "jackpot": 73270242.96, "outcome": "Roll"},
        {"draw_date": "2025-01-07", "main_numbers": [9, 12, 27, 39, 42], "powerball": 18, "jackpot": 66277347.09, "outcome": "Roll"},
        {"draw_date": "2025-01-03", "main_numbers": [6, 9, 10, 25, 47], "powerball": 1, "jackpot": 60614591.68, "outcome": "Roll"},
    ]
    
    print(f"📊 Processing {len(powerball_2025_data)} PowerBall 2025 draws...")
    
    # Convert to DataFrame
    df = pd.DataFrame(powerball_2025_data)
    
    # Add game type and draw day
    df['game_type'] = 'PowerBall'
    df['draw_day'] = pd.to_datetime(df['draw_date']).dt.strftime('%A')
    df['source'] = 'real_data_2025'
    
    # Ensure data directory exists
    os.makedirs('data', exist_ok=True)
    
    # Save PowerBall 2025 data
    powerball_file = 'data/powerball_2025_data.csv'
    df.to_csv(powerball_file, index=False)
    print(f"✅ Saved PowerBall 2025 data to {powerball_file}")
    
    # Show summary
    print(f"\n📈 PowerBall 2025 Summary:")
    print(f"   Total draws: {len(df)}")
    print(f"   Date range: {df['draw_date'].min()} to {df['draw_date'].max()}")
    print(f"   Won draws: {len(df[df['outcome'] == 'Won'])}")
    print(f"   Roll draws: {len(df[df['outcome'] == 'Roll'])}")
    print(f"   Average jackpot: R{df['jackpot'].mean():,.2f}")
    print(f"   Max jackpot: R{df['jackpot'].max():,.2f}")
    
    # Show sample draws
    print(f"\n📋 Sample draws:")
    for i, row in df.head(5).iterrows():
        print(f"   {i+1}. {row['draw_date']} - {row['main_numbers']} + {row['powerball']} (R{row['jackpot']:,.2f}) - {row['outcome']}")
    
    return df

if __name__ == "__main__":
    process_powerball_2025_data()

