#!/usr/bin/env python3

import sys
import os

# Add current directory to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def test_advanced_scraper():
    """Test the advanced scraper"""
    print("🚀 Testing Advanced PowerBall Scraper")
    print("=" * 50)
    
    try:
        from advanced_web_scraper import AdvancedPowerBallScraper
        
        scraper = AdvancedPowerBallScraper()
        print("✅ Scraper initialized")
        
        # Test the scraper
        print("\n🔍 Attempting to collect real data...")
        result = scraper.collect_real_data()
        
        if result:
            print(f"🎉 SUCCESS! Collected {len(result)} real draws")
            
            # Show sample
            print("\n📋 Sample of real data:")
            for i, draw in enumerate(result[:3]):
                print(f"  {i+1}. {draw['draw_date']} - {draw['main_numbers']} + {draw['powerball']} ({draw['game_type']})")
            
            return True
        else:
            print("❌ No real data collected")
            return False
            
    except ImportError as e:
        print(f"❌ Import error: {e}")
        return False
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = test_advanced_scraper()
    
    if not success:
        print("\n" + "=" * 50)
        print("⚠️  Advanced scraping failed")
        print("\n📝 Next steps:")
        print("1. You can provide screenshots of the historical data")
        print("2. I'll help you enter the data manually")
        print("3. Or we can use the sample data for now")
        print("\nTo start manual data entry:")
        print("  C:\\Python313\\python.exe manual_data_entry.py")

