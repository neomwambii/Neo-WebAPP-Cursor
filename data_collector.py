import requests
from bs4 import BeautifulSoup
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import time
import json
import os
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import re

class PowerBallDataCollector:
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
        
    def setup_driver(self):
        """Setup Chrome driver for web scraping"""
        chrome_options = Options()
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument("--window-size=1920,1080")
        
        service = Service(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service, options=chrome_options)
        return driver
    
    def parse_draw_date(self, date_str):
        """Parse various date formats from the website"""
        try:
            # Try different date formats
            formats = [
                "%d %B %Y",
                "%d %b %Y", 
                "%d/%m/%Y",
                "%Y-%m-%d"
            ]
            
            for fmt in formats:
                try:
                    return datetime.strptime(date_str.strip(), fmt)
                except ValueError:
                    continue
            
            # If all formats fail, try to extract date from string
            date_match = re.search(r'(\d{1,2})[\/\-](\d{1,2})[\/\-](\d{4})', date_str)
            if date_match:
                day, month, year = date_match.groups()
                return datetime(int(year), int(month), int(day))
                
        except Exception as e:
            print(f"Error parsing date '{date_str}': {e}")
            
        return None
    
    def collect_powerball_data(self, start_year=2020):
        """Collect PowerBall historical data"""
        print("Collecting PowerBall data...")
        
        driver = self.setup_driver()
        all_draws = []
        
        try:
            # Navigate to PowerBall results page
            url = f"{self.base_url}/powerball"
            driver.get(url)
            
            # Wait for page to load
            WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CLASS_NAME, "results-table"))
            )
            
            # Scroll to load more historical data
            last_height = driver.execute_script("return document.body.scrollHeight")
            scroll_attempts = 0
            max_scrolls = 20
            
            while scroll_attempts < max_scrolls:
                # Scroll down
                driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                time.sleep(2)
                
                # Check if new content loaded
                new_height = driver.execute_script("return document.body.scrollHeight")
                if new_height == last_height:
                    break
                last_height = new_height
                scroll_attempts += 1
            
            # Extract draw data
            draw_elements = driver.find_elements(By.CSS_SELECTOR, ".draw-item, .result-item, tr")
            
            for element in draw_elements:
                try:
                    # Extract draw information
                    draw_data = self.extract_draw_data(element)
                    if draw_data and self.is_valid_draw(draw_data):
                        all_draws.append(draw_data)
                except Exception as e:
                    continue
            
            print(f"Collected {len(all_draws)} PowerBall draws")
            
        except Exception as e:
            print(f"Error collecting PowerBall data: {e}")
        finally:
            driver.quit()
        
        # Save to CSV
        if all_draws:
            df = pd.DataFrame(all_draws)
            df = df.sort_values('draw_date', ascending=False)
            df.to_csv(self.powerball_file, index=False)
            print(f"PowerBall data saved to {self.powerball_file}")
        
        return all_draws
    
    def collect_powerball_plus_data(self, start_year=2020):
        """Collect PowerBall Plus historical data"""
        print("Collecting PowerBall Plus data...")
        
        driver = self.setup_driver()
        all_draws = []
        
        try:
            # Navigate to PowerBall Plus results page
            url = f"{self.base_url}/powerball-plus"
            driver.get(url)
            
            # Wait for page to load
            WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CLASS_NAME, "results-table"))
            )
            
            # Scroll to load more historical data
            last_height = driver.execute_script("return document.body.scrollHeight")
            scroll_attempts = 0
            max_scrolls = 20
            
            while scroll_attempts < max_scrolls:
                driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                time.sleep(2)
                
                new_height = driver.execute_script("return document.body.scrollHeight")
                if new_height == last_height:
                    break
                last_height = new_height
                scroll_attempts += 1
            
            # Extract draw data
            draw_elements = driver.find_elements(By.CSS_SELECTOR, ".draw-item, .result-item, tr")
            
            for element in draw_elements:
                try:
                    draw_data = self.extract_draw_data(element, is_plus=True)
                    if draw_data and self.is_valid_draw(draw_data):
                        all_draws.append(draw_data)
                except Exception as e:
                    continue
            
            print(f"Collected {len(all_draws)} PowerBall Plus draws")
            
        except Exception as e:
            print(f"Error collecting PowerBall Plus data: {e}")
        finally:
            driver.quit()
        
        # Save to CSV
        if all_draws:
            df = pd.DataFrame(all_draws)
            df = df.sort_values('draw_date', ascending=False)
            df.to_csv(self.powerball_plus_file, index=False)
            print(f"PowerBall Plus data saved to {self.powerball_plus_file}")
        
        return all_draws
    
    def extract_draw_data(self, element, is_plus=False):
        """Extract draw data from a single element"""
        try:
            # Get text content
            text = element.text.strip()
            if not text:
                return None
            
            # Look for date pattern
            date_match = re.search(r'(\d{1,2}[\/\-]\d{1,2}[\/\-]\d{4}|\d{1,2}\s+\w+\s+\d{4})', text)
            if not date_match:
                return None
            
            draw_date = self.parse_draw_date(date_match.group(1))
            if not draw_date:
                return None
            
            # Extract numbers
            numbers = re.findall(r'\b(\d{1,2})\b', text)
            if len(numbers) < 6:  # Need at least 5 main numbers + 1 powerball
                return None
            
            # Convert to integers
            numbers = [int(n) for n in numbers]
            
            # Separate main numbers and powerball
            main_numbers = sorted(numbers[:5])
            powerball = numbers[5]
            
            # Validate number ranges
            if not all(self.main_numbers_range[0] <= n <= self.main_numbers_range[1] for n in main_numbers):
                return None
            if not (self.powerball_range[0] <= powerball <= self.powerball_range[1]):
                return None
            
            return {
                'draw_date': draw_date,
                'main_numbers': main_numbers,
                'powerball': powerball,
                'game_type': 'PowerBall Plus' if is_plus else 'PowerBall',
                'draw_day': draw_date.strftime('%A')
            }
            
        except Exception as e:
            return None
    
    def is_valid_draw(self, draw_data):
        """Validate if draw data is complete and correct"""
        if not draw_data:
            return False
        
        required_fields = ['draw_date', 'main_numbers', 'powerball', 'game_type']
        if not all(field in draw_data for field in required_fields):
            return False
        
        if len(draw_data['main_numbers']) != 5:
            return False
        
        if not all(self.main_numbers_range[0] <= n <= self.main_numbers_range[1] for n in draw_data['main_numbers']):
            return False
        
        if not (self.powerball_range[0] <= draw_data['powerball'] <= self.powerball_range[1]):
            return False
        
        return True
    
    def collect_all_data(self):
        """Collect all historical data"""
        print("Starting data collection...")
        
        # Collect PowerBall data
        powerball_data = self.collect_powerball_data()
        
        # Collect PowerBall Plus data
        powerball_plus_data = self.collect_powerball_plus_data()
        
        # Combine and save all data
        all_data = powerball_data + powerball_plus_data
        if all_data:
            df = pd.DataFrame(all_data)
            df = df.sort_values('draw_date', ascending=False)
            combined_file = os.path.join(self.data_dir, "all_powerball_data.csv")
            df.to_csv(combined_file, index=False)
            print(f"All data saved to {combined_file}")
        
        return all_data
    
    def get_latest_data(self):
        """Get the most recent data from files"""
        data = []
        
        if os.path.exists(self.powerball_file):
            df = pd.read_csv(self.powerball_file)
            data.extend(df.to_dict('records'))
        
        if os.path.exists(self.powerball_plus_file):
            df = pd.read_csv(self.powerball_plus_file)
            data.extend(df.to_dict('records'))
        
        return data

if __name__ == "__main__":
    collector = PowerBallDataCollector()
    collector.collect_all_data()

