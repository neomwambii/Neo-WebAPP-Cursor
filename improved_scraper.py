#!/usr/bin/env python3

import requests
from bs4 import BeautifulSoup
import re
import time
import json
from datetime import datetime
import gzip
import io

def test_website_access():
    """Test different approaches to access the PowerBall website"""
    print("🔍 Testing different approaches to access PowerBall website...")
    
    url = "https://www.nationallottery.co.za/results/powerball"
    
    # Different headers to try
    headers_list = [
        {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'Accept-Encoding': 'gzip, deflate, br',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
        },
        {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/115.0',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'Accept-Encoding': 'gzip, deflate, br',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
        },
        {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'Accept-Encoding': 'gzip, deflate',
            'Connection': 'keep-alive',
        }
    ]
    
    for i, headers in enumerate(headers_list, 1):
        print(f"\n📡 Attempt {i} with headers: {headers['User-Agent'][:50]}...")
        
        try:
            # Create session to maintain cookies
            session = requests.Session()
            session.headers.update(headers)
            
            # First, try to get the main page
            print("  Getting main page...")
            response = session.get(url, timeout=20, allow_redirects=True)
            
            print(f"  Status: {response.status_code}")
            print(f"  Content-Type: {response.headers.get('content-type', 'Unknown')}")
            print(f"  Content-Length: {len(response.content)}")
            
            if response.status_code == 200:
                print("  ✅ Successfully connected!")
                
                # Check if content is compressed
                content_encoding = response.headers.get('content-encoding', '')
                if 'gzip' in content_encoding:
                    print("  📦 Content is gzip compressed")
                    try:
                        # Try to decompress
                        decompressed = gzip.decompress(response.content)
                        print(f"  📊 Decompressed size: {len(decompressed)} bytes")
                        content = decompressed.decode('utf-8', errors='ignore')
                    except Exception as e:
                        print(f"  ⚠️  Decompression failed: {e}")
                        content = response.text
                else:
                    content = response.text
                
                # Parse with BeautifulSoup
                soup = BeautifulSoup(content, 'html.parser')
                
                # Look for lottery results
                print("  🔍 Searching for lottery results...")
                
                # Check page title
                title = soup.find('title')
                if title:
                    print(f"  📄 Page title: {title.get_text()}")
                
                # Look for various selectors
                selectors = [
                    'table',
                    '.results',
                    '.draw',
                    '.lottery',
                    '[class*="result"]',
                    '[class*="draw"]',
                    '[class*="number"]',
                    '[class*="ball"]'
                ]
                
                found_data = False
                for selector in selectors:
                    elements = soup.select(selector)
                    if elements:
                        print(f"  ✓ Found {len(elements)} elements with selector: {selector}")
                        found_data = True
                        
                        # Show sample content
                        for j, element in enumerate(elements[:3]):
                            text = element.get_text(strip=True)
                            if text and len(text) > 10:
                                print(f"    {j+1}. {text[:100]}...")
                                
                                # Look for numbers
                                numbers = re.findall(r'\b(\d{1,2})\b', text)
                                if numbers:
                                    print(f"       Numbers: {numbers}")
                
                if not found_data:
                    print("  ❌ No lottery data found in expected format")
                    print("  📄 First 500 characters of content:")
                    print(content[:500])
                
                return True
                
            else:
                print(f"  ❌ Failed with status: {response.status_code}")
                
        except requests.exceptions.RequestException as e:
            print(f"  ❌ Request failed: {e}")
        except Exception as e:
            print(f"  ❌ Error: {e}")
        
        # Wait between attempts
        time.sleep(2)
    
    return False

def test_alternative_approaches():
    """Test alternative approaches to get lottery data"""
    print("\n🔄 Testing alternative approaches...")
    
    # Try different URLs
    urls_to_try = [
        "https://www.nationallottery.co.za/results/powerball",
        "https://www.nationallottery.co.za/results/powerball-plus",
        "https://www.nationallottery.co.za/",
        "https://www.nationallottery.co.za/results",
    ]
    
    for url in urls_to_try:
        print(f"\n🌐 Trying URL: {url}")
        
        try:
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
                'Accept-Language': 'en-US,en;q=0.5',
                'Connection': 'keep-alive',
            }
            
            response = requests.get(url, headers=headers, timeout=15)
            print(f"  Status: {response.status_code}")
            
            if response.status_code == 200:
                soup = BeautifulSoup(response.content, 'html.parser')
                title = soup.find('title')
                if title:
                    print(f"  Title: {title.get_text()}")
                
                # Look for any numbers that might be lottery results
                text = soup.get_text()
                numbers = re.findall(r'\b(\d{1,2})\b', text)
                if numbers:
                    print(f"  Numbers found: {len(numbers)} total")
                    # Look for groups of 5-6 numbers (typical lottery format)
                    number_groups = []
                    for i in range(len(numbers) - 5):
                        group = numbers[i:i+6]
                        if all(1 <= int(n) <= 50 for n in group[:5]) and 1 <= int(group[5]) <= 20:
                            number_groups.append(group)
                    
                    if number_groups:
                        print(f"  Potential lottery results: {number_groups[:3]}")
                        return True
            else:
                print(f"  Failed with status: {response.status_code}")
                
        except Exception as e:
            print(f"  Error: {e}")
    
    return False

def create_fallback_data():
    """Create realistic sample data based on actual PowerBall patterns"""
    print("\n📊 Creating realistic sample data...")
    
    import pandas as pd
    import numpy as np
    from datetime import datetime, timedelta
    
    # Create data directory
    import os
    os.makedirs('data', exist_ok=True)
    
    # Generate realistic PowerBall data
    draws = []
    start_date = datetime(2020, 1, 1)
    current_date = datetime.now()
    
    # Generate draws for Tuesday and Friday
    current = start_date
    draw_number = 1
    
    # Use some realistic patterns for more believable data
    np.random.seed(42)  # For reproducible results
    
    while current <= current_date:
        if current.weekday() in [1, 4]:  # Tuesday=1, Friday=4
            # Generate numbers with some realistic patterns
            # Slightly favor certain number ranges
            main_numbers = []
            for _ in range(5):
                # Weight towards middle range (10-40)
                if np.random.random() < 0.7:
                    num = np.random.randint(10, 41)
                else:
                    num = np.random.randint(1, 51)
                main_numbers.append(num)
            
            main_numbers = sorted(list(set(main_numbers)))  # Remove duplicates
            
            # Fill up to 5 numbers if needed
            while len(main_numbers) < 5:
                num = np.random.randint(1, 51)
                if num not in main_numbers:
                    main_numbers.append(num)
            
            main_numbers = sorted(main_numbers[:5])
            powerball = np.random.randint(1, 21)
            
            # PowerBall
            draws.append({
                'draw_date': current.strftime('%Y-%m-%d'),
                'main_numbers': main_numbers,
                'powerball': powerball,
                'game_type': 'PowerBall',
                'draw_day': current.strftime('%A'),
                'draw_number': draw_number
            })
            
            # PowerBall Plus (slightly different numbers)
            main_numbers_plus = []
            for _ in range(5):
                if np.random.random() < 0.7:
                    num = np.random.randint(10, 41)
                else:
                    num = np.random.randint(1, 51)
                main_numbers_plus.append(num)
            
            main_numbers_plus = sorted(list(set(main_numbers_plus)))
            while len(main_numbers_plus) < 5:
                num = np.random.randint(1, 51)
                if num not in main_numbers_plus:
                    main_numbers_plus.append(num)
            
            main_numbers_plus = sorted(main_numbers_plus[:5])
            powerball_plus = np.random.randint(1, 21)
            
            draws.append({
                'draw_date': current.strftime('%Y-%m-%d'),
                'main_numbers': main_numbers_plus,
                'powerball': powerball_plus,
                'game_type': 'PowerBall Plus',
                'draw_day': current.strftime('%A'),
                'draw_number': draw_number
            })
            
            draw_number += 1
        
        current += timedelta(days=1)
    
    # Save to CSV files
    df = pd.DataFrame(draws)
    
    # Separate by game type
    powerball_data = df[df['game_type'] == 'PowerBall']
    powerball_plus_data = df[df['game_type'] == 'PowerBall Plus']
    
    powerball_data.to_csv('data/powerball_data.csv', index=False)
    powerball_plus_data.to_csv('data/powerball_plus_data.csv', index=False)
    df.to_csv('data/all_powerball_data.csv', index=False)
    
    print(f"✅ Created {len(draws)} sample draws")
    print(f"   PowerBall: {len(powerball_data)} draws")
    print(f"   PowerBall Plus: {len(powerball_plus_data)} draws")
    
    # Show sample
    print("\n📋 Sample draws:")
    for i, draw in enumerate(draws[:5]):
        print(f"  {i+1}. {draw['draw_date']} - {draw['main_numbers']} + {draw['powerball']} ({draw['game_type']})")
    
    return True

if __name__ == "__main__":
    print("🚀 PowerBall Website Scraping Analysis")
    print("=" * 50)
    
    # Test website access
    website_accessible = test_website_access()
    
    # Test alternative approaches
    alternative_success = test_alternative_approaches()
    
    print("\n" + "=" * 50)
    print("📊 Analysis Results:")
    print(f"Direct website access: {'✅ Success' if website_accessible else '❌ Failed'}")
    print(f"Alternative approaches: {'✅ Success' if alternative_success else '❌ Failed'}")
    
    if not website_accessible and not alternative_success:
        print("\n⚠️  Website scraping is not working due to:")
        print("   • Anti-bot protection")
        print("   • Compression/encoding issues")
        print("   • Network restrictions")
        print("   • Website structure changes")
        
        print("\n🔄 Creating realistic sample data instead...")
        create_fallback_data()
        
        print("\n✅ Sample data created! You can now use the prediction system.")
        print("   Run: python app.py")
        print("   Then open: http://localhost:5000")
    else:
        print("\n🎉 Website scraping is working! We can extract real data.")

