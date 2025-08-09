#!/usr/bin/env python3
"""
CFP Rankings Scraper v2 - Properly handles the dropdown selectors

This version correctly uses the year and week dropdown selectors found on the CFP website.
"""

import time
import json
import pandas as pd
from datetime import datetime
from typing import Dict, List, Optional
import logging
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from bs4 import BeautifulSoup

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('cfp_scraper_v2.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)


class CFPRankingsScraperV2:
    """CFP Rankings Scraper that properly uses dropdown selectors."""
    
    def __init__(self, headless: bool = True, wait_time: int = 10):
        """Initialize the scraper."""
        self.base_url = "https://collegefootballplayoff.com/rankings.aspx"
        self.wait_time = wait_time
        self.headless = headless
        self.driver = None
        
    def _setup_driver(self) -> webdriver.Chrome:
        """Set up Chrome WebDriver."""
        logger.info("Setting up Chrome WebDriver...")
        
        chrome_options = Options()
        if self.headless:
            chrome_options.add_argument("--headless")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument("--window-size=1920,1080")
        
        try:
            driver = webdriver.Chrome(options=chrome_options)
            logger.info("ChromeDriver initialized successfully")
            return driver
        except Exception as e:
            logger.error(f"Failed to initialize ChromeDriver: {e}")
            raise

    def _get_available_years(self) -> List[str]:
        """Get available years from the dropdown."""
        try:
            select_elements = self.driver.find_elements(By.TAG_NAME, "select")
            
            if len(select_elements) >= 1:
                # First select should be years
                year_select = Select(select_elements[0])
                years = [option.text.strip() for option in year_select.options if option.text.strip()]
                logger.info(f"Found years: {years}")
                return years
            else:
                logger.warning("No select elements found for years")
                return []
        except Exception as e:
            logger.error(f"Error getting available years: {e}")
            return []

    def _get_available_weeks(self) -> List[str]:
        """Get available weeks from the dropdown."""
        try:
            select_elements = self.driver.find_elements(By.TAG_NAME, "select")
            
            if len(select_elements) >= 2:
                # Second select should be weeks
                week_select = Select(select_elements[1])
                weeks = [option.text.strip() for option in week_select.options if option.text.strip()]
                logger.info(f"Found weeks: {weeks}")
                return weeks
            else:
                logger.warning("No select elements found for weeks")
                return []
        except Exception as e:
            logger.error(f"Error getting available weeks: {e}")
            return []

    def _select_year_and_week(self, year: str, week: str) -> bool:
        """Select specific year and week from dropdowns."""
        try:
            logger.info(f"Selecting year: {year}, week: {week}")
            
            select_elements = self.driver.find_elements(By.TAG_NAME, "select")
            
            if len(select_elements) >= 2:
                # Select year (first dropdown)
                year_select = Select(select_elements[0])
                year_select.select_by_visible_text(year)
                time.sleep(2)
                
                # Select week (second dropdown)
                week_select = Select(select_elements[1])
                week_select.select_by_visible_text(week)
                time.sleep(3)  # Wait for page to update
                
                logger.info(f"Successfully selected {year}, {week}")
                return True
            else:
                logger.error("Not enough select elements found")
                return False
                
        except Exception as e:
            logger.error(f"Error selecting {year}, {week}: {e}")
            return False

    def _extract_rankings_from_current_page(self, year: str, week: str) -> List[Dict]:
        """Extract rankings from the currently loaded page."""
        logger.info(f"Extracting rankings for {year}, {week}...")
        
        rankings_data = []
        
        try:
            # Wait a bit for content to load
            time.sleep(3)
            
            # Get page source and parse with BeautifulSoup
            page_source = self.driver.page_source
            soup = BeautifulSoup(page_source, 'html.parser')
            
            # Look for ranking tables
            tables = soup.find_all('table')
            
            for table in tables:
                rows = table.find_all('tr')
                
                for row in rows:
                    cells = row.find_all(['td', 'th'])
                    
                    if len(cells) >= 3:
                        # Try to extract rank from first cell
                        rank_text = cells[0].get_text(strip=True)
                        
                        # Skip header rows
                        if rank_text.lower() in ['rank', '#', 'ranking', 'rnk']:
                            continue
                            
                        try:
                            # Clean rank text and convert to int
                            rank_clean = rank_text.replace('#', '').replace('.', '').strip()
                            rank = int(rank_clean)
                            
                            # Validate rank range
                            if not (1 <= rank <= 25):
                                continue
                                
                        except (ValueError, TypeError):
                            continue
                        
                        # Extract team name (usually in 2nd or 3rd cell)
                        team_name = ""
                        for i in range(1, min(4, len(cells))):
                            cell_text = cells[i].get_text(strip=True)
                            # Clean up team name
                            cell_text = cell_text.replace('Logo', '').replace('logo', '').strip()
                            
                            # Skip cells with just numbers or short text
                            if cell_text and len(cell_text) > 2 and not cell_text.isdigit():
                                team_name = cell_text
                                break
                        
                        # Extract record (look for pattern like "12-1", "10-2")
                        record = ""
                        for cell in cells[1:6]:  # Check multiple cells for record
                            cell_text = cell.get_text(strip=True)
                            # Look for record pattern (numbers-numbers)
                            if '-' in cell_text and len(cell_text) <= 8:
                                # Validate it looks like a record
                                parts = cell_text.split('-')
                                if len(parts) == 2 and all(part.isdigit() for part in parts):
                                    record = cell_text
                                    break
                        
                        # Only add if we have valid data
                        if team_name and 1 <= rank <= 25:
                            ranking_entry = {
                                'year': int(year),
                                'week': week,
                                'rank': rank,
                                'team': team_name,
                                'record': record,
                                'scraped_at': datetime.now().isoformat()
                            }
                            rankings_data.append(ranking_entry)
                            logger.debug(f"Added: #{rank} {team_name} ({record})")
            
            # If no data found in tables, try alternative methods
            if not rankings_data:
                logger.warning(f"No rankings found in tables for {year}, {week}")
                
                # Try to find rankings in other formats (divs, lists, etc.)
                ranking_divs = soup.find_all('div', class_=lambda x: x and ('rank' in x.lower() or 'team' in x.lower()))
                
                # This would need more specific parsing based on actual site structure
                # For now, we'll rely on table parsing
            
            logger.info(f"Extracted {len(rankings_data)} rankings for {year}, {week}")
            
        except Exception as e:
            logger.error(f"Error extracting rankings for {year}, {week}: {e}")
        
        return rankings_data

    def scrape_year(self, year: str) -> List[Dict]:
        """Scrape all available weeks for a specific year."""
        logger.info(f"Scraping year {year}...")
        
        year_data = []
        
        if not self.driver:
            self.driver = self._setup_driver()
        
        try:
            # Navigate to main rankings page
            self.driver.get(self.base_url)
            time.sleep(5)
            
            # Get available weeks for this year
            weeks = self._get_available_weeks()
            
            for week in weeks:
                try:
                    # Select year and week
                    if self._select_year_and_week(year, week):
                        # Extract rankings
                        week_rankings = self._extract_rankings_from_current_page(year, week)
                        year_data.extend(week_rankings)
                        
                        logger.info(f"Year {year}, {week}: {len(week_rankings)} rankings")
                        
                        # Small delay between weeks
                        time.sleep(2)
                    else:
                        logger.warning(f"Failed to select {year}, {week}")
                        
                except Exception as e:
                    logger.error(f"Error scraping {year}, {week}: {e}")
                    continue
            
        except Exception as e:
            logger.error(f"Error scraping year {year}: {e}")
        
        return year_data

    def scrape_all_years(self, start_year: int = 2014, end_year: int = None) -> List[Dict]:
        """Scrape all years of rankings data."""
        if end_year is None:
            end_year = datetime.now().year
            
        logger.info(f"Starting scrape from {start_year} to {end_year}")
        
        all_data = []
        
        try:
            self.driver = self._setup_driver()
            
            # Get list of available years from the website
            self.driver.get(self.base_url)
            time.sleep(5)
            
            available_years = self._get_available_years()
            
            # Filter years based on requested range
            target_years = [year for year in available_years 
                          if start_year <= int(year) <= end_year]
            
            logger.info(f"Will scrape years: {target_years}")
            
            for year in target_years:
                try:
                    year_data = self.scrape_year(year)
                    all_data.extend(year_data)
                    logger.info(f"Year {year} complete: {len(year_data)} rankings")
                    
                    # Longer pause between years
                    time.sleep(5)
                    
                except Exception as e:
                    logger.error(f"Failed to scrape year {year}: {e}")
                    continue
            
        except Exception as e:
            logger.error(f"Error during scraping: {e}")
        finally:
            if self.driver:
                self.driver.quit()
        
        logger.info(f"Scraping completed. Total: {len(all_data)} rankings")
        return all_data

    def export_to_csv(self, data: List[Dict], filename: str = None) -> str:
        """Export data to CSV."""
        if not filename:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"cfp_rankings_v2_{timestamp}.csv"
        
        df = pd.DataFrame(data)
        if not df.empty:
            # Sort by year, week order, then rank
            df = df.sort_values(['year', 'week', 'rank'])
        
        filepath = f"/Users/mainamusa/Documents/Personal/CFB Data/cfp-ranking-predictor/{filename}"
        df.to_csv(filepath, index=False)
        
        logger.info(f"Data exported to {filepath}")
        return filepath

    def export_by_year(self, data: List[Dict]) -> List[str]:
        """Export separate CSV files for each year."""
        files_created = []
        
        if not data:
            return files_created
        
        df = pd.DataFrame(data)
        
        for year in df['year'].unique():
            year_data = df[df['year'] == year]
            filename = f"cfp_rankings_{year}_fixed.csv"
            
            filepath = f"/Users/mainamusa/Documents/Personal/CFB Data/cfp-ranking-predictor/{filename}"
            year_data.to_csv(filepath, index=False)
            
            files_created.append(filepath)
            logger.info(f"Created {filename}: {len(year_data)} rankings")
        
        return files_created


def main():
    """Main function to run the scraper."""
    scraper = CFPRankingsScraperV2(headless=True)
    
    try:
        # Scrape all available data
        print("Starting CFP rankings scrape...")
        data = scraper.scrape_all_years()
        
        if data:
            print(f"\nSuccessfully collected {len(data)} rankings!")
            
            # Export main file
            main_csv = scraper.export_to_csv(data)
            print(f"Main CSV: {main_csv}")
            
            # Export by year
            year_files = scraper.export_by_year(data)
            print(f"Year files: {len(year_files)} created")
            
            # Show summary
            df = pd.DataFrame(data)
            print(f"\nSummary:")
            print(f"Years: {sorted(df['year'].unique())}")
            print(f"Weeks per year: {df.groupby('year')['week'].nunique().to_dict()}")
            print(f"Teams in rankings: {df['team'].nunique()}")
            
        else:
            print("No data collected. Check logs for errors.")
            
    except Exception as e:
        print(f"Error: {e}")
        logger.error(f"Main execution error: {e}")


if __name__ == "__main__":
    main()
