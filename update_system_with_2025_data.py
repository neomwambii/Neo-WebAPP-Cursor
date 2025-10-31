#!/usr/bin/env python3

import pandas as pd
import os
from datetime import datetime

def update_system_with_2025_data():
    """Update the system to use 2025 PowerBall data"""
    print("🚀 Updating PowerBall system with 2025 data...")
    
    # Load 2025 PowerBall data
    powerball_2025 = pd.read_csv('data/powerball_2025_data.csv')
    print(f"✅ Loaded {len(powerball_2025)} PowerBall 2025 draws")
    
    # Update the main data files
    powerball_2025.to_csv('data/powerball_data.csv', index=False)
    powerball_2025.to_csv('data/all_powerball_data.csv', index=False)
    
    print(f"✅ Updated system with 2025 PowerBall data")
    print(f"   Date range: {powerball_2025['draw_date'].min()} to {powerball_2025['draw_date'].max()}")
    print(f"   Won draws: {len(powerball_2025[powerball_2025['outcome'] == 'Won'])}")
    print(f"   Roll draws: {len(powerball_2025[powerball_2025['outcome'] == 'Roll'])}")
    
    # Show sample
    print(f"\n📋 Sample 2025 draws:")
    for i, row in powerball_2025.head(3).iterrows():
        print(f"   {i+1}. {row['draw_date']} - {row['main_numbers']} + {row['powerball']} (R{row['jackpot']:,.0f}) - {row['outcome']}")
    
    return powerball_2025

if __name__ == "__main__":
    update_system_with_2025_data()

