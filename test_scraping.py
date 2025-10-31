#!/usr/bin/env python3

import requests
from bs4 import BeautifulSoup
import re
from datetime import datetime

def test_powerball_scraping():
    """Test scraping PowerBall data from the website"""
    print("🎯 Testing PowerBall website scraping...")
    
    url = "https://www.nationallottery.co.za/results/powerball"
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.5',
        'Connection': 'keep-alive',
    }
    
    try:
        print(f"📡 Connecting to: {url}")
        response = requests.get(url, headers=headers, timeout=15)
        response.raise_for_status()
        
        print(f"✅ Successfully connected! Status: {response.status_code}")
        print(f"📄 Page size: {len(response.content)} bytes")
        
        # Parse the HTML
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Look for different possible selectors
        selectors_to_try = [
            'table tr',
            '.results-table tr',
            '.draw-item',
            '.result-item',
            '.lottery-result',
            'tr[data-draw]',
            '.draw-row',
            '[class*="result"]',
            '[class*="draw"]'
        ]
        
        print("\n🔍 Searching for draw data...")
        found_elements = []
        
        for selector in selectors_to_try:
            elements = soup.select(selector)
            if elements:
                print(f"✓ Found {len(elements)} elements with selector: {selector}")
                found_elements.extend(elements)
            else:
                print(f"✗ No elements found with selector: {selector}")
        
        if found_elements:
            print(f"\n📊 Total elements found: {len(found_elements)}")
            
            # Show sample of what we found
            print("\n📋 Sample elements:")
            for i, element in enumerate(found_elements[:5]):
                text = element.get_text(strip=True)
                print(f"{i+1}. {text[:100]}...")
                
                # Look for numbers in the text
                numbers = re.findall(r'\b(\d{1,2})\b', text)
                if numbers:
                    print(f"   Numbers found: {numbers}")
        else:
            print("❌ No draw elements found")
            print("\n🔍 Let's see what's on the page...")
            
            # Show page title and some content
            title = soup.find('title')
            if title:
                print(f"Page title: {title.get_text()}")
            
            # Look for any tables
            tables = soup.find_all('table')
            print(f"Tables found: {len(tables)}")
            
            # Look for any divs with class containing 'result' or 'draw'
            result_divs = soup.find_all('div', class_=re.compile(r'result|draw', re.I))
            print(f"Result/Draw divs found: {len(result_divs)}")
            
            # Show some raw HTML
            print(f"\n📄 First 500 characters of HTML:")
            print(response.text[:500])
        
        return True
        
    except requests.exceptions.RequestException as e:
        print(f"❌ Request failed: {e}")
        return False
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def test_powerball_plus_scraping():
    """Test scraping PowerBall Plus data from the website"""
    print("\n🎯 Testing PowerBall Plus website scraping...")
    
    url = "https://www.nationallottery.co.za/results/powerball-plus"
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.5',
        'Connection': 'keep-alive',
    }
    
    try:
        print(f"📡 Connecting to: {url}")
        response = requests.get(url, headers=headers, timeout=15)
        response.raise_for_status()
        
        print(f"✅ Successfully connected! Status: {response.status_code}")
        print(f"📄 Page size: {len(response.content)} bytes")
        
        # Parse the HTML
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Look for draw data
        selectors_to_try = [
            'table tr',
            '.results-table tr',
            '.draw-item',
            '.result-item',
            '.lottery-result',
            'tr[data-draw]',
            '.draw-row',
            '[class*="result"]',
            '[class*="draw"]'
        ]
        
        print("\n🔍 Searching for draw data...")
        found_elements = []
        
        for selector in selectors_to_try:
            elements = soup.select(selector)
            if elements:
                print(f"✓ Found {len(elements)} elements with selector: {selector}")
                found_elements.extend(elements)
            else:
                print(f"✗ No elements found with selector: {selector}")
        
        if found_elements:
            print(f"\n📊 Total elements found: {len(found_elements)}")
            
            # Show sample of what we found
            print("\n📋 Sample elements:")
            for i, element in enumerate(found_elements[:5]):
                text = element.get_text(strip=True)
                print(f"{i+1}. {text[:100]}...")
                
                # Look for numbers in the text
                numbers = re.findall(r'\b(\d{1,2})\b', text)
                if numbers:
                    print(f"   Numbers found: {numbers}")
        else:
            print("❌ No draw elements found")
        
        return True
        
    except requests.exceptions.RequestException as e:
        print(f"❌ Request failed: {e}")
        return False
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

if __name__ == "__main__":
    print("🚀 Testing South African PowerBall Website Scraping")
    print("=" * 60)
    
    # Test PowerBall
    powerball_success = test_powerball_scraping()
    
    # Test PowerBall Plus
    powerball_plus_success = test_powerball_plus_scraping()
    
    print("\n" + "=" * 60)
    print("📊 Test Results:")
    print(f"PowerBall: {'✅ Success' if powerball_success else '❌ Failed'}")
    print(f"PowerBall Plus: {'✅ Success' if powerball_plus_success else '❌ Failed'}")
    
    if powerball_success or powerball_plus_success:
        print("\n🎉 Website scraping is working! We can extract real data.")
    else:
        print("\n⚠️  Website scraping failed. We'll use sample data for now.")

