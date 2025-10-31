import requests
from bs4 import BeautifulSoup
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import time
import json
import os
import re

class SimplePowerBallCollector:
    def __init__(self):
        self.base_url = "https://www.nationallottery.co.za/results"
        self.data_dir = "data"
        self.powerball_file = os.path.join(self.data_dir, "powerball_data.csv")
        self.powerball_plus_file = os.path.join(self.data_dir, "powerball_plus_data.csv")
        
        # Ensure data directory exists
        os.makedirs(self.data_dir, exist_ok=True)
        
        # PowerBall number ranges
        self.main_numbers_range = (1, 50)  # 5 numbers from 1-50
        self.powerball_range = (1, 20)     # 1 powerball from 1-20
        
    def create_sample_data(self):
        """Create sample data for testing when web scraping fails"""
        print("Creating sample data for testing...")
        
        # Generate sample PowerBall data
        powerball_data = []
        powerball_plus_data = []
        
        # Start from 2020
        start_date = datetime(2020, 1, 1)
        current_date = datetime.now()
        
        # Generate draws for Tuesday and Friday
        current = start_date
        draw_number = 1
        
        while current <= current_date:
            # Check if it's Tuesday (1) or Friday (4)
            if current.weekday() in [1, 4]:  # Tuesday=1, Friday=4
                # Generate random but realistic numbers
                main_numbers = sorted(np.random.choice(range(1, 51), 5, replace=False))
                powerball = np.random.choice(range(1, 21))
                
                draw_data = {
                    'draw_date': current.strftime('%Y-%m-%d'),
                    'main_numbers': main_numbers,
                    'powerball': powerball,
                    'game_type': 'PowerBall',
                    'draw_day': current.strftime('%A'),
                    'draw_number': draw_number
                }
                powerball_data.append(draw_data)
                
                # PowerBall Plus (slightly different numbers)
                main_numbers_plus = sorted(np.random.choice(range(1, 51), 5, replace=False))
                powerball_plus = np.random.choice(range(1, 21))
                
                draw_data_plus = {
                    'draw_date': current.strftime('%Y-%m-%d'),
                    'main_numbers': main_numbers_plus,
                    'powerball': powerball_plus,
                    'game_type': 'PowerBall Plus',
                    'draw_day': current.strftime('%A'),
                    'draw_number': draw_number
                }
                powerball_plus_data.append(draw_data_plus)
                
                draw_number += 1
            
            current += timedelta(days=1)
        
        # Save PowerBall data
        if powerball_data:
            df_pb = pd.DataFrame(powerball_data)
            df_pb.to_csv(self.powerball_file, index=False)
            print(f"Created {len(powerball_data)} PowerBall draws")
        
        # Save PowerBall Plus data
        if powerball_plus_data:
            df_pbp = pd.DataFrame(powerball_plus_data)
            df_pbp.to_csv(self.powerball_plus_file, index=False)
            print(f"Created {len(powerball_plus_data)} PowerBall Plus draws")
        
        # Create combined data
        all_data = powerball_data + powerball_plus_data
        if all_data:
            df_all = pd.DataFrame(all_data)
            combined_file = os.path.join(self.data_dir, "all_powerball_data.csv")
            df_all.to_csv(combined_file, index=False)
            print(f"Combined data saved to {combined_file}")
        
        return all_data
    
    def try_web_scraping(self):
        """Try to scrape real data from the website"""
        print("Attempting to collect real data from website...")
        
        try:
            # Try to get PowerBall data
            url = f"{self.base_url}/powerball"
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
            }
            
            response = requests.get(url, headers=headers, timeout=10)
            if response.status_code == 200:
                print("Successfully connected to PowerBall website")
                # Here you would parse the HTML to extract draw data
                # For now, we'll fall back to sample data
                return self.create_sample_data()
            else:
                print(f"Failed to connect to website. Status code: {response.status_code}")
                return self.create_sample_data()
                
        except Exception as e:
            print(f"Web scraping failed: {e}")
            print("Falling back to sample data...")
            return self.create_sample_data()
    
    def collect_data(self):
        """Main method to collect data"""
        print("Starting PowerBall data collection...")
        
        # First try web scraping
        data = self.try_web_scraping()
        
        print(f"Data collection complete. Total draws: {len(data)}")
        return data

if __name__ == "__main__":
    collector = SimplePowerBallCollector()
    collector.collect_data()

