#!/usr/bin/env python3

import requests
from bs4 import BeautifulSoup
import time
import json
import re
from datetime import datetime
import pandas as pd

def try_alternative_data_sources():
    """Try alternative ways to get real PowerBall data"""
    print("🔍 Searching for alternative data sources...")
    
    # Try different approaches
    approaches = [
        {
            'name': 'Direct API endpoints',
            'urls': [
                'https://www.nationallottery.co.za/api/results',
                'https://www.nationallottery.co.za/api/powerball',
                'https://www.nationallottery.co.za/api/lottery',
                'https://www.nationallottery.co.za/results.json',
                'https://www.nationallottery.co.za/data/results',
            ]
        },
        {
            'name': 'Mobile/API versions',
            'urls': [
                'https://m.nationallottery.co.za/results/powerball',
                'https://api.nationallottery.co.za/results',
                'https://www.nationallottery.co.za/mobile/results',
            ]
        },
        {
            'name': 'Alternative lottery data sites',
            'urls': [
                'https://www.lottery.co.za/powerball-results',
                'https://www.sa-lottery.co.za/powerball',
                'https://lotteryresults.co.za/powerball',
            ]
        }
    ]
    
    for approach in approaches:
        print(f"\n📡 Trying {approach['name']}...")
        
        for url in approach['urls']:
            try:
                print(f"  Testing: {url}")
                response = requests.get(url, timeout=10)
                print(f"    Status: {response.status_code}")
                
                if response.status_code == 200:
                    # Check if it's JSON
                    try:
                        data = response.json()
                        print(f"    ✅ JSON data found! Keys: {list(data.keys())}")
                        return url, data
                    except:
                        # Check if it's HTML with lottery data
                        soup = BeautifulSoup(response.content, 'html.parser')
                        text = soup.get_text()
                        numbers = re.findall(r'\b(\d{1,2})\b', text)
                        if len(numbers) > 10:  # Likely lottery data
                            print(f"    ✅ HTML with lottery data found! {len(numbers)} numbers")
                            return url, soup
                
            except Exception as e:
                print(f"    ❌ Error: {e}")
    
    return None, None

def try_manual_data_entry():
    """Provide instructions for manual data entry"""
    print("\n📝 Manual Data Entry Option")
    print("=" * 40)
    
    print("Since automated scraping isn't working, you can manually add real data:")
    print("\n1. Visit: https://www.nationallottery.co.za/results/powerball")
    print("2. Copy the recent results")
    print("3. Use this format to add them:")
    
    sample_format = """
    # Add this to a file called 'manual_data.csv'
    draw_date,main_numbers,powerball,game_type,draw_day
    2024-01-15,"[1, 5, 12, 23, 45]",8,PowerBall,Tuesday
    2024-01-12,"[3, 7, 18, 29, 41]",15,PowerBall,Friday
    """
    
    print(sample_format)
    
    # Create a template file
    template_data = [
        ['draw_date', 'main_numbers', 'powerball', 'game_type', 'draw_day'],
        ['2024-01-15', '[1, 5, 12, 23, 45]', '8', 'PowerBall', 'Tuesday'],
        ['2024-01-12', '[3, 7, 18, 29, 41]', '15', 'PowerBall', 'Friday'],
        ['2024-01-09', '[2, 8, 14, 27, 39]', '12', 'PowerBall', 'Tuesday'],
    ]
    
    df = pd.DataFrame(template_data[1:], columns=template_data[0])
    df.to_csv('manual_data_template.csv', index=False)
    print("✅ Created 'manual_data_template.csv' for you to fill in")

def check_existing_data():
    """Check what data we currently have"""
    print("\n📊 Current Data Status")
    print("=" * 30)
    
    data_files = [
        'data/powerball_data.csv',
        'data/powerball_plus_data.csv',
        'data/all_powerball_data.csv'
    ]
    
    for file_path in data_files:
        try:
            if os.path.exists(file_path):
                df = pd.read_csv(file_path)
                print(f"✅ {file_path}")
                print(f"   Rows: {len(df)}")
                print(f"   Columns: {list(df.columns)}")
                
                # Check if it's sample data by looking at patterns
                if 'raw_text' in df.columns:
                    print("   📝 Contains sample data markers")
                else:
                    print("   🤔 Data source unclear")
                
                # Show sample
                if len(df) > 0:
                    sample = df.iloc[0]
                    print(f"   Sample: {sample['draw_date']} - {sample['main_numbers']} + {sample['powerball']}")
            else:
                print(f"❌ {file_path} (not found)")
        except Exception as e:
            print(f"❌ {file_path} - Error: {e}")

def create_real_data_collector():
    """Create a tool for collecting real data manually"""
    print("\n🛠️ Creating Real Data Collection Tool")
    print("=" * 40)
    
    collector_code = '''
# Real Data Collector Tool
# Use this to manually add real PowerBall results

import pandas as pd
from datetime import datetime
import os

def add_real_draw(draw_date, main_numbers, powerball, game_type="PowerBall"):
    """Add a real draw to the data"""
    # Ensure data directory exists
    os.makedirs('data', exist_ok=True)
    
    # Create draw data
    draw_data = {
        'draw_date': draw_date,
        'main_numbers': main_numbers,
        'powerball': powerball,
        'game_type': game_type,
        'draw_day': datetime.strptime(draw_date, '%Y-%m-%d').strftime('%A')
    }
    
    # Load existing data
    file_path = 'data/all_powerball_data.csv'
    if os.path.exists(file_path):
        df = pd.read_csv(file_path)
    else:
        df = pd.DataFrame()
    
    # Add new draw
    new_row = pd.DataFrame([draw_data])
    df = pd.concat([df, new_row], ignore_index=True)
    
    # Remove duplicates and sort
    df = df.drop_duplicates(subset=['draw_date', 'game_type'])
    df = df.sort_values('draw_date', ascending=False)
    
    # Save
    df.to_csv(file_path, index=False)
    print(f"✅ Added {game_type} draw: {draw_date} - {main_numbers} + {powerball}")
    
    return df

# Example usage:
# add_real_draw('2024-01-15', [1, 5, 12, 23, 45], 8, 'PowerBall')
# add_real_draw('2024-01-12', [3, 7, 18, 29, 41], 15, 'PowerBall')
'''
    
    with open('real_data_collector.py', 'w') as f:
        f.write(collector_code)
    
    print("✅ Created 'real_data_collector.py' for manual data entry")

if __name__ == "__main__":
    import os
    
    print("🎯 PowerBall Real Data Analysis")
    print("=" * 50)
    
    # Check current data
    check_existing_data()
    
    # Try alternative sources
    url, data = try_alternative_data_sources()
    
    if url and data:
        print(f"\n🎉 Found real data source: {url}")
        print("We can now collect actual historical data!")
    else:
        print("\n⚠️ No alternative data sources found")
        print("We'll need to use sample data or manual entry")
        
        # Create manual data entry tools
        try_manual_data_entry()
        create_real_data_collector()
        
        print("\n📋 Options for getting real data:")
        print("1. Use the sample data (realistic but not real)")
        print("2. Manually add real results using the template")
        print("3. Try to find other data sources")
        print("4. Contact the lottery for official data access")

