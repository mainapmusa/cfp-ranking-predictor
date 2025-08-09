#!/usr/bin/env python3
"""
Site inspector to understand the CFP website structure.
"""

import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By

def inspect_cfp_site():
    """Inspect the CFP website to understand its structure."""
    chrome_options = Options()
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    
    driver = webdriver.Chrome(options=chrome_options)
    
    try:
        # Visit main rankings page
        print("Visiting main rankings page...")
        driver.get("https://collegefootballplayoff.com/rankings.aspx")
        time.sleep(5)
        
        print("Page title:", driver.title)
        print("Current URL:", driver.current_url)
        
        # Look for selectors and navigation
        selects = driver.find_elements(By.TAG_NAME, "select")
        print(f"Found {len(selects)} select elements")
        
        for i, select in enumerate(selects):
            print(f"  Select {i}: {select.get_attribute('id')} / {select.get_attribute('class')}")
            options = select.find_elements(By.TAG_NAME, "option")
            for j, option in enumerate(options[:5]):  # Show first 5 options
                print(f"    Option {j}: {option.text}")
        
        # Look for links that might contain years
        links = driver.find_elements(By.TAG_NAME, "a")
        year_links = [link for link in links if link.text and any(str(year) in link.text for year in range(2014, 2025))]
        
        print(f"\nFound {len(year_links)} year-related links:")
        for link in year_links[:10]:  # Show first 10
            print(f"  {link.text} -> {link.get_attribute('href')}")
        
        # Check for specific 2024 content
        print("\nChecking for 2024 content...")
        try:
            driver.get("https://collegefootballplayoff.com/news/2024/12/8/cfp-rankings-241208.aspx")
            time.sleep(3)
            print("2024 rankings page title:", driver.title)
            
            # Look for ranking tables
            tables = driver.find_elements(By.TAG_NAME, "table")
            print(f"Found {len(tables)} tables on 2024 page")
            
            if tables:
                first_table = tables[0]
                rows = first_table.find_elements(By.TAG_NAME, "tr")
                print(f"First table has {len(rows)} rows")
                
                for i, row in enumerate(rows[:5]):  # Show first 5 rows
                    cells = row.find_elements(By.TAG_NAME, "td")
                    if cells:
                        cell_texts = [cell.text.strip() for cell in cells]
                        print(f"  Row {i}: {cell_texts}")
                        
        except Exception as e:
            print(f"Error accessing 2024 page: {e}")
        
        # Save page source for inspection
        with open("cfp_page_source.html", "w") as f:
            f.write(driver.page_source)
        print("\nPage source saved to cfp_page_source.html")
        
    finally:
        driver.quit()

if __name__ == "__main__":
    inspect_cfp_site()
