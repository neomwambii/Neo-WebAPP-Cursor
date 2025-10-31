import requests
from bs4 import BeautifulSoup
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import time
import json
import os
import re
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import warnings
warnings.filterwarnings('ignore')

class RealPowerBallCollector:
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
        
        # Headers for web requests
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'Accept-Encoding': 'gzip, deflate',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
        }
        
    def setup_driver(self):
        """Setup Chrome driver for web scraping"""
        try:
            chrome_options = Options()
            chrome_options.add_argument("--headless")
            chrome_options.add_argument("--no-sandbox")
            chrome_options.add_argument("--disable-dev-shm-usage")
            chrome_options.add_argument("--disable-gpu")
            chrome_options.add_argument("--window-size=1920,1080")
            chrome_options.add_argument("--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36")
            
            service = Service(ChromeDriverManager().install())
            driver = webdriver.Chrome(service=service, options=chrome_options)
            return driver
        except Exception as e:
            print(f"Error setting up Chrome driver: {e}")
            return None
    
    def try_requests_scraping(self, url):
        """Try to scrape using requests and BeautifulSoup"""
        try:
            print(f"Trying requests method for: {url}")
            response = requests.get(url, headers=self.headers, timeout=15)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.content, 'html.parser')
            print(f"✓ Successfully loaded page with requests")
            return soup
        except Exception as e:
            print(f"Requests method failed: {e}")
            return None
    
    def try_selenium_scraping(self, url):
        """Try to scrape using Selenium"""
        try:
            print(f"Trying Selenium method for: {url}")
            driver = self.setup_driver()
            if not driver:
                return None
                
            driver.get(url)
            time.sleep(3)  # Wait for page to load
            
            # Try to scroll to load more content
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(2)
            
            soup = BeautifulSoup(driver.page_source, 'html.parser')
            driver.quit()
            print(f"✓ Successfully loaded page with Selenium")
            return soup
        except Exception as e:
            print(f"Selenium method failed: {e}")
            return None
    
    def parse_draw_date(self, date_str):
        """Parse various date formats from the website"""
        try:
            # Clean the date string
            date_str = date_str.strip().replace('\n', ' ').replace('\t', ' ')
            date_str = re.sub(r'\s+', ' ', date_str)  # Remove extra spaces
            
            # Try different date formats
            formats = [
                "%d %B %Y",      # 15 January 2024
                "%d %b %Y",      # 15 Jan 2024
                "%d/%m/%Y",      # 15/01/2024
                "%Y-%m-%d",      # 2024-01-15
                "%d-%m-%Y",      # 15-01-2024
                "%B %d, %Y",     # January 15, 2024
                "%b %d, %Y",     # Jan 15, 2024
            ]
            
            for fmt in formats:
                try:
                    return datetime.strptime(date_str, fmt)
                except ValueError:
                    continue
            
            # If all formats fail, try to extract date from string
            date_match = re.search(r'(\d{1,2})[\/\-](\d{1,2})[\/\-](\d{4})', date_str)
            if date_match:
                day, month, year = date_match.groups()
                return datetime(int(year), int(month), int(day))
            
            # Try to extract from text like "15 January 2024"
            month_names = {
                'january': 1, 'february': 2, 'march': 3, 'april': 4,
                'may': 5, 'june': 6, 'july': 7, 'august': 8,
                'september': 9, 'october': 10, 'november': 11, 'december': 12
            }
            
            for month_name, month_num in month_names.items():
                if month_name in date_str.lower():
                    # Extract day and year
                    day_match = re.search(r'(\d{1,2})', date_str)
                    year_match = re.search(r'(\d{4})', date_str)
                    if day_match and year_match:
                        return datetime(int(year_match.group(1)), month_num, int(day_match.group(1)))
                
        except Exception as e:
            print(f"Error parsing date '{date_str}': {e}")
            
        return None
    
    def extract_numbers_from_text(self, text):
        """Extract numbers from text content"""
        # Find all numbers in the text
        numbers = re.findall(r'\b(\d{1,2})\b', text)
        numbers = [int(n) for n in numbers if n.isdigit()]
        
        # Filter numbers by range
        main_numbers = [n for n in numbers if self.main_numbers_range[0] <= n <= self.main_numbers_range[1]]
        powerballs = [n for n in numbers if self.powerball_range[0] <= n <= self.powerball_range[1]]
        
        return main_numbers, powerballs
    
    def scrape_powerball_data(self):
        """Scrape PowerBall data from the website"""
        print("🎯 Scraping PowerBall data...")
        
        url = f"{self.base_url}/powerball"
        soup = self.try_requests_scraping(url)
        
        if not soup:
            soup = self.try_selenium_scraping(url)
        
        if not soup:
            print("❌ Failed to load PowerBall page")
            return []
        
        draws = []
        
        # Look for different possible selectors
        selectors = [
            '.results-table tr',
            '.draw-item',
            '.result-item',
            '.lottery-result',
            'tr[data-draw]',
            '.draw-row',
            'table tr'
        ]
        
        for selector in selectors:
            elements = soup.select(selector)
            if elements:
                print(f"Found {len(elements)} elements with selector: {selector}")
                break
        
        if not elements:
            print("No draw elements found, trying alternative approach...")
            # Try to find any table or list of results
            tables = soup.find_all('table')
            if tables:
                elements = tables[0].find_all('tr')
                print(f"Found {len(elements)} table rows")
        
        for element in elements:
            try:
                draw_data = self.extract_draw_from_element(element, 'PowerBall')
                if draw_data:
                    draws.append(draw_data)
            except Exception as e:
                continue
        
        print(f"✓ Extracted {len(draws)} PowerBall draws")
        return draws
    
    def scrape_powerball_plus_data(self):
        """Scrape PowerBall Plus data from the website"""
        print("🎯 Scraping PowerBall Plus data...")
        
        url = f"{self.base_url}/powerball-plus"
        soup = self.try_requests_scraping(url)
        
        if not soup:
            soup = self.try_selenium_scraping(url)
        
        if not soup:
            print("❌ Failed to load PowerBall Plus page")
            return []
        
        draws = []
        
        # Look for different possible selectors
        selectors = [
            '.results-table tr',
            '.draw-item',
            '.result-item',
            '.lottery-result',
            'tr[data-draw]',
            '.draw-row',
            'table tr'
        ]
        
        for selector in selectors:
            elements = soup.select(selector)
            if elements:
                print(f"Found {len(elements)} elements with selector: {selector}")
                break
        
        if not elements:
            print("No draw elements found, trying alternative approach...")
            tables = soup.find_all('table')
            if tables:
                elements = tables[0].find_all('tr')
                print(f"Found {len(elements)} table rows")
        
        for element in elements:
            try:
                draw_data = self.extract_draw_from_element(element, 'PowerBall Plus')
                if draw_data:
                    draws.append(draw_data)
            except Exception as e:
                continue
        
        print(f"✓ Extracted {len(draws)} PowerBall Plus draws")
        return draws
    
    def extract_draw_from_element(self, element, game_type):
        """Extract draw data from a single element"""
        try:
            text = element.get_text(strip=True)
            if not text or len(text) < 10:  # Skip empty or very short elements
                return None
            
            # Look for date patterns
            date_patterns = [
                r'(\d{1,2}[\/\-]\d{1,2}[\/\-]\d{4})',
                r'(\d{1,2}\s+\w+\s+\d{4})',
                r'(\w+\s+\d{1,2},?\s+\d{4})',
                r'(\d{4}[\/\-]\d{1,2}[\/\-]\d{1,2})'
            ]
            
            draw_date = None
            for pattern in date_patterns:
                date_match = re.search(pattern, text)
                if date_match:
                    draw_date = self.parse_draw_date(date_match.group(1))
                    if draw_date:
                        break
            
            if not draw_date:
                return None
            
            # Extract numbers
            main_numbers, powerballs = self.extract_numbers_from_text(text)
            
            # Validate we have the right number of numbers
            if len(main_numbers) >= 5 and len(powerballs) >= 1:
                # Take first 5 main numbers and first powerball
                main_numbers = sorted(main_numbers[:5])
                powerball = powerballs[0]
                
                # Validate ranges
                if all(self.main_numbers_range[0] <= n <= self.main_numbers_range[1] for n in main_numbers):
                    if self.powerball_range[0] <= powerball <= self.powerball_range[1]:
                        return {
                            'draw_date': draw_date,
                            'main_numbers': main_numbers,
                            'powerball': powerball,
                            'game_type': game_type,
                            'draw_day': draw_date.strftime('%A'),
                            'raw_text': text[:100]  # Store first 100 chars for debugging
                        }
            
        except Exception as e:
            return None
        
        return None
    
    def collect_all_data(self):
        """Collect all historical data from both websites"""
        print("🚀 Starting real data collection from South African National Lottery...")
        print("=" * 70)
        
        all_draws = []
        
        # Collect PowerBall data
        powerball_draws = self.scrape_powerball_data()
        all_draws.extend(powerball_draws)
        
        # Collect PowerBall Plus data
        powerball_plus_draws = self.scrape_powerball_plus_data()
        all_draws.extend(powerball_plus_draws)
        
        # Save individual files
        if powerball_draws:
            df_pb = pd.DataFrame(powerball_draws)
            df_pb = df_pb.sort_values('draw_date', ascending=False)
            df_pb.to_csv(self.powerball_file, index=False)
            print(f"💾 Saved {len(powerball_draws)} PowerBall draws to {self.powerball_file}")
        
        if powerball_plus_draws:
            df_pbp = pd.DataFrame(powerball_plus_draws)
            df_pbp = df_pbp.sort_values('draw_date', ascending=False)
            df_pbp.to_csv(self.powerball_plus_file, index=False)
            print(f"💾 Saved {len(powerball_plus_draws)} PowerBall Plus draws to {self.powerball_plus_file}")
        
        # Save combined data
        if all_draws:
            df_all = pd.DataFrame(all_draws)
            df_all = df_all.sort_values('draw_date', ascending=False)
            combined_file = os.path.join(self.data_dir, "all_powerball_data.csv")
            df_all.to_csv(combined_file, index=False)
            print(f"💾 Saved {len(all_draws)} total draws to {combined_file}")
            
            # Show sample of collected data
            print("\n📊 Sample of collected data:")
            print("-" * 50)
            for i, draw in enumerate(all_draws[:5]):
                print(f"{i+1}. {draw['draw_date'].strftime('%Y-%m-%d')} - {draw['main_numbers']} + {draw['powerball']} ({draw['game_type']})")
        
        print(f"\n✅ Data collection complete! Total draws: {len(all_draws)}")
        return all_draws

if __name__ == "__main__":
    collector = RealPowerBallCollector()
    collector.collect_all_data()

