#!/usr/bin/env python3
"""
Test the CFP scraper with a single year to verify it works correctly.
"""

from cfp_scraper import CFPRankingsScraper
import pandas as pd

def test_single_year():
    """Test scraping a single year."""
    scraper = CFPRankingsScraper(headless=False)  # Show browser for debugging
    
    try:
        print("Testing 2022 scraping...")
        data_2022 = scraper.scrape_year("2022")
        
        if data_2022:
            print(f"Successfully scraped {len(data_2022)} rankings for 2022!")
            
            # Show sample data
            print("\nSample rankings:")
            for i, entry in enumerate(data_2022[:10]):
                print(f"{entry['week']} - #{entry['rank']} {entry['team']} ({entry['record']})")
            
            # Export to test CSV
            df = pd.DataFrame(data_2022)
            csv_file = "/Users/mainamusa/Documents/Personal/CFB Data/cfp-ranking-predictor/test_2022_rankings.csv"
            df.to_csv(csv_file, index=False)
            print(f"\nTest data saved to: {csv_file}")
            
            # Check data quality
            print(f"\nData quality check:")
            print(f"Years represented: {df['year'].unique()}")
            print(f"Weeks represented: {df['week'].unique()}")
            print(f"Rank range: {df['rank'].min()} to {df['rank'].max()}")
            print(f"Teams: {df['team'].nunique()} unique teams")
            
        else:
            print("No data found for 2022")
            
    except Exception as e:
        print(f"Error: {e}")
    finally:
        if scraper.driver:
            scraper.driver.quit()

if __name__ == "__main__":
    test_single_year()
