#!/usr/bin/env python3
"""
Test the CFP scraper v2 with a single year to verify it works correctly.
"""

from cfp_scraper_v2 import CFPRankingsScraperV2
import pandas as pd

def test_single_year():
    """Test scraping a single year."""
    scraper = CFPRankingsScraperV2(headless=False)  # Show browser for debugging
    
    try:
        print("Testing 2023 scraping...")
        data_2023 = scraper.scrape_year("2023")
        
        if data_2023:
            print(f"Successfully scraped {len(data_2023)} rankings for 2023!")
            
            # Show sample data
            print("\nSample rankings:")
            for i, entry in enumerate(data_2023[:10]):
                print(f"{entry['week']} - #{entry['rank']} {entry['team']} ({entry['record']})")
            
            # Export to test CSV
            df = pd.DataFrame(data_2023)
            csv_file = "/Users/mainamusa/Documents/Personal/CFB Data/cfp-ranking-predictor/test_2023_rankings.csv"
            df.to_csv(csv_file, index=False)
            print(f"\nTest data saved to: {csv_file}")
            
            # Check data quality
            print(f"\nData quality check:")
            print(f"Years represented: {df['year'].unique()}")
            print(f"Weeks represented: {df['week'].unique()}")
            print(f"Rank range: {df['rank'].min()} to {df['rank'].max()}")
            print(f"Teams: {df['team'].nunique()} unique teams")
            
        else:
            print("No data found for 2023")
            
    except Exception as e:
        print(f"Error: {e}")
    finally:
        if scraper.driver:
            scraper.driver.quit()

if __name__ == "__main__":
    test_single_year()
