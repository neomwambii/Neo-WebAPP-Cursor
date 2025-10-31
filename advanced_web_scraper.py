#!/usr/bin/env python3

import requests
from bs4 import BeautifulSoup
import time
import random
import json
import re
from datetime import datetime
import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from webdriver_manager.chrome import ChromeDriverManager
import warnings
warnings.filterwarnings('ignore')

class AdvancedPowerBallScraper:
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
        
    def setup_stealth_driver(self):
        """Setup Chrome driver with stealth features"""
        try:
            chrome_options = Options()
            
            # Stealth options
            chrome_options.add_argument("--disable-blink-features=AutomationControlled")
            chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
            chrome_options.add_experimental_option('useAutomationExtension', False)
            
            # Normal browser options
            chrome_options.add_argument("--no-sandbox")
            chrome_options.add_argument("--disable-dev-shm-usage")
            chrome_options.add_argument("--disable-gpu")
            chrome_options.add_argument("--window-size=1920,1080")
            chrome_options.add_argument("--start-maximized")
            
            # User agent
            chrome_options.add_argument("--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36")
            
            # Additional stealth
            chrome_options.add_argument("--disable-web-security")
            chrome_options.add_argument("--allow-running-insecure-content")
            chrome_options.add_argument("--disable-extensions")
            chrome_options.add_argument("--disable-plugins")
            chrome_options.add_argument("--disable-images")  # Faster loading
            
            service = Service(ChromeDriverManager().install())
            driver = webdriver.Chrome(service=service, options=chrome_options)
            
            # Execute stealth script
            driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
            
            return driver
        except Exception as e:
            print(f"Error setting up stealth driver: {e}")
            return None
    
    def try_requests_with_rotation(self):
        """Try requests with different approaches"""
        print("🔄 Trying requests with rotation...")
        
        # Different user agents
        user_agents = [
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/115.0',
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Edge/120.0.0.0'
        ]
        
        # Different headers
        headers_list = [
            {
                'User-Agent': random.choice(user_agents),
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
                'Accept-Language': 'en-US,en;q=0.5',
                'Accept-Encoding': 'gzip, deflate, br',
                'Connection': 'keep-alive',
                'Upgrade-Insecure-Requests': '1',
                'Sec-Fetch-Dest': 'document',
                'Sec-Fetch-Mode': 'navigate',
                'Sec-Fetch-Site': 'none',
                'Cache-Control': 'max-age=0'
            },
            {
                'User-Agent': random.choice(user_agents),
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
                'Accept-Language': 'en-US,en;q=0.5',
                'Connection': 'keep-alive',
                'Referer': 'https://www.google.com/'
            }
        ]
        
        urls_to_try = [
            f"{self.base_url}/powerball",
            f"{self.base_url}/powerball-plus",
            f"{self.base_url}/",
            "https://www.nationallottery.co.za/",
        ]
        
        for url in urls_to_try:
            print(f"  Testing: {url}")
            
            for i, headers in enumerate(headers_list):
                try:
                    print(f"    Attempt {i+1} with headers...")
                    
                    # Create session
                    session = requests.Session()
                    session.headers.update(headers)
                    
                    # Add random delay
                    time.sleep(random.uniform(1, 3))
                    
                    # Make request
                    response = session.get(url, timeout=20, allow_redirects=True)
                    
                    print(f"    Status: {response.status_code}")
                    print(f"    Content-Type: {response.headers.get('content-type', 'Unknown')}")
                    print(f"    Content-Length: {len(response.content)}")
                    
                    if response.status_code == 200:
                        # Check if we got lottery data
                        soup = BeautifulSoup(response.content, 'html.parser')
                        text = soup.get_text()
                        
                        # Look for lottery numbers
                        numbers = re.findall(r'\b(\d{1,2})\b', text)
                        if len(numbers) > 20:  # Likely lottery data
                            print(f"    ✅ Found potential lottery data! {len(numbers)} numbers")
                            
                            # Try to extract draws
                            draws = self.extract_draws_from_soup(soup, url)
                            if draws:
                                print(f"    ✅ Extracted {len(draws)} draws!")
                                return draws
                        
                        print(f"    ⚠️  No clear lottery data found")
                    
                except Exception as e:
                    print(f"    ❌ Error: {e}")
                
                time.sleep(random.uniform(2, 5))  # Random delay between attempts
        
        return []
    
    def try_selenium_stealth(self):
        """Try Selenium with stealth features"""
        print("🕵️ Trying Selenium with stealth...")
        
        driver = self.setup_stealth_driver()
        if not driver:
            return []
        
        try:
            urls_to_try = [
                f"{self.base_url}/powerball",
                f"{self.base_url}/powerball-plus"
            ]
            
            all_draws = []
            
            for url in urls_to_try:
                print(f"  Testing: {url}")
                
                try:
                    # Navigate to page
                    driver.get(url)
                    
                    # Wait for page to load
                    time.sleep(random.uniform(3, 6))
                    
                    # Scroll to load content
                    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                    time.sleep(2)
                    
                    # Try to find and click "Load More" or similar buttons
                    try:
                        load_more_selectors = [
                            "button[class*='load']",
                            "a[class*='more']",
                            "button[class*='show']",
                            ".load-more",
                            ".show-more"
                        ]
                        
                        for selector in load_more_selectors:
                            try:
                                load_more = driver.find_element(By.CSS_SELECTOR, selector)
                                if load_more.is_displayed():
                                    print(f"    Found load more button: {selector}")
                                    driver.execute_script("arguments[0].click();", load_more)
                                    time.sleep(3)
                                    break
                            except:
                                continue
                    except:
                        pass
                    
                    # Get page source
                    soup = BeautifulSoup(driver.page_source, 'html.parser')
                    
                    # Extract draws
                    draws = self.extract_draws_from_soup(soup, url)
                    if draws:
                        print(f"    ✅ Extracted {len(draws)} draws from {url}")
                        all_draws.extend(draws)
                    else:
                        print(f"    ❌ No draws found in {url}")
                    
                    # Random delay between pages
                    time.sleep(random.uniform(2, 5))
                    
                except Exception as e:
                    print(f"    ❌ Error with {url}: {e}")
            
            return all_draws
            
        finally:
            driver.quit()
    
    def extract_draws_from_soup(self, soup, url):
        """Extract draws from BeautifulSoup object"""
        draws = []
        
        # Determine game type from URL
        game_type = "PowerBall Plus" if "plus" in url.lower() else "PowerBall"
        
        # Try different selectors
        selectors_to_try = [
            'table tr',
            '.results-table tr',
            '.draw-item',
            '.result-item',
            '.lottery-result',
            'tr[data-draw]',
            '.draw-row',
            '[class*="result"]',
            '[class*="draw"]',
            '.number',
            '.ball'
        ]
        
        for selector in selectors_to_try:
            elements = soup.select(selector)
            if elements:
                print(f"    Found {len(elements)} elements with selector: {selector}")
                
                for element in elements:
                    try:
                        draw_data = self.extract_draw_from_element(element, game_type)
                        if draw_data:
                            draws.append(draw_data)
                    except Exception as e:
                        continue
                
                if draws:
                    break
        
        return draws
    
    def extract_draw_from_element(self, element, game_type):
        """Extract draw data from a single element"""
        try:
            text = element.get_text(strip=True)
            if not text or len(text) < 10:
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
                            'source': 'web_scraping'
                        }
            
        except Exception as e:
            return None
        
        return None
    
    def parse_draw_date(self, date_str):
        """Parse various date formats"""
        try:
            date_str = date_str.strip().replace('\n', ' ').replace('\t', ' ')
            date_str = re.sub(r'\s+', ' ', date_str)
            
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
            
            # Try to extract date from string
            date_match = re.search(r'(\d{1,2})[\/\-](\d{1,2})[\/\-](\d{4})', date_str)
            if date_match:
                day, month, year = date_match.groups()
                return datetime(int(year), int(month), int(day))
                
        except Exception as e:
            pass
            
        return None
    
    def extract_numbers_from_text(self, text):
        """Extract numbers from text content"""
        numbers = re.findall(r'\b(\d{1,2})\b', text)
        numbers = [int(n) for n in numbers if n.isdigit()]
        
        main_numbers = [n for n in numbers if self.main_numbers_range[0] <= n <= self.main_numbers_range[1]]
        powerballs = [n for n in numbers if self.powerball_range[0] <= n <= self.powerball_range[1]]
        
        return main_numbers, powerballs
    
    def collect_real_data(self):
        """Main method to collect real data using advanced techniques"""
        print("🚀 Advanced PowerBall Data Collection")
        print("=" * 50)
        
        all_draws = []
        
        # Try requests first
        print("\n1. Trying advanced requests...")
        draws = self.try_requests_with_rotation()
        if draws:
            print(f"✅ Requests method found {len(draws)} draws")
            all_draws.extend(draws)
        else:
            print("❌ Requests method failed")
        
        # Try Selenium if requests failed
        if not all_draws:
            print("\n2. Trying Selenium stealth...")
            draws = self.try_selenium_stealth()
            if draws:
                print(f"✅ Selenium method found {len(draws)} draws")
                all_draws.extend(draws)
            else:
                print("❌ Selenium method failed")
        
        # Save data if we found any
        if all_draws:
            print(f"\n💾 Saving {len(all_draws)} real draws...")
            
            # Separate by game type
            powerball_draws = [d for d in all_draws if d['game_type'] == 'PowerBall']
            powerball_plus_draws = [d for d in all_draws if d['game_type'] == 'PowerBall Plus']
            
            # Save individual files
            if powerball_draws:
                df_pb = pd.DataFrame(powerball_draws)
                df_pb = df_pb.sort_values('draw_date', ascending=False)
                df_pb.to_csv(self.powerball_file, index=False)
                print(f"✅ Saved {len(powerball_draws)} PowerBall draws")
            
            if powerball_plus_draws:
                df_pbp = pd.DataFrame(powerball_plus_draws)
                df_pbp = df_pbp.sort_values('draw_date', ascending=False)
                df_pbp.to_csv(self.powerball_plus_file, index=False)
                print(f"✅ Saved {len(powerball_plus_draws)} PowerBall Plus draws")
            
            # Save combined data
            df_all = pd.DataFrame(all_draws)
            df_all = df_all.sort_values('draw_date', ascending=False)
            combined_file = os.path.join(self.data_dir, "all_powerball_data.csv")
            df_all.to_csv(combined_file, index=False)
            print(f"✅ Saved {len(all_draws)} total draws to {combined_file}")
            
            # Show sample
            print(f"\n📋 Sample of real data:")
            for i, draw in enumerate(all_draws[:5]):
                print(f"  {i+1}. {draw['draw_date'].strftime('%Y-%m-%d')} - {draw['main_numbers']} + {draw['powerball']} ({draw['game_type']})")
            
            return all_draws
        else:
            print("\n❌ No real data could be collected")
            return []

if __name__ == "__main__":
    import os
    scraper = AdvancedPowerBallScraper()
    scraper.collect_real_data()

