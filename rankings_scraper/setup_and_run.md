# CFP Rankings Scraper Setup and Usage

This scraper collects all historical College Football Playoff (CFP) rankings data from the official CFP website and saves it to CSV files.

## Setup Instructions

### 1. Install Python Dependencies

First, install the required Python packages:

```bash
pip install -r requirements.txt
```

### 2. Install Chrome Browser

The scraper uses Chrome WebDriver, so you need Google Chrome installed:
- **Mac**: Download from [chrome.google.com](https://www.google.com/chrome/)
- **Windows**: Download from [chrome.google.com](https://www.google.com/chrome/)
- **Linux**: Use your package manager or download from Google

### 3. Verify Installation

You can test that everything is set up correctly by running:

```bash
python -c "from selenium import webdriver; from webdriver_manager.chrome import ChromeDriverManager; print('Setup successful!')"
```

## Running the Scraper

### Quick Start (Recommended)

To scrape all historical data and save to CSV files:

```bash
python run_scraper.py
```

This will:
- Scrape all CFP rankings from 2014 to present
- Save one main CSV file with all data
- Save separate CSV files for each year
- Display summary statistics
- Create log files for debugging

### Advanced Usage

For more control, you can use the scraper directly:

```python
from cfp_scraper import CFPRankingsScraper

# Create scraper
scraper = CFPRankingsScraper(headless=True)

# Scrape specific years
data = scraper.scrape_all_historical_data(start_year=2020, end_year=2023)

# Save to CSV
csv_file = scraper.export_to_csv(data, "my_cfp_data.csv")
```

## Output Files

The scraper creates several files:

### CSV Files
- `cfp_rankings_all_data_YYYYMMDD_HHMMSS.csv` - All historical data
- `cfp_rankings_2014.csv` - 2014 season data
- `cfp_rankings_2015.csv` - 2015 season data
- ... (one file per year)

### Log Files
- `cfp_scraper.log` - Detailed scraping logs for debugging

## CSV File Format

Each CSV file contains the following columns:

| Column | Description | Example |
|--------|-------------|---------|
| year | Season year | 2023 |
| week | Week description | "Week 12", "Final" |
| rank | Team ranking (1-25) | 1 |
| team | Team name | "Georgia" |
| record | Win-loss record | "12-1" |
| scraped_at | When data was collected | "2024-01-15T10:30:00" |

## Troubleshooting

### Common Issues

1. **Chrome not found**: Install Google Chrome browser
2. **Permission errors**: Run with appropriate permissions
3. **Network timeouts**: Check internet connection, try increasing wait_time
4. **No data collected**: Website might have changed structure

### Debug Mode

To see the browser in action (helpful for debugging):

```python
scraper = CFPRankingsScraper(headless=False)  # Shows browser window
```

### Check Logs

Always check `cfp_scraper.log` for detailed error information:

```bash
tail -f cfp_scraper.log
```

## Data Notes

- CFP rankings started in 2014
- Rankings are typically released weekly during the season (October-December)
- Final rankings determine playoff participants
- Team names are extracted as they appear on the official website
- Some weeks may not have rankings (bye weeks, off-season)

## Performance

- Full historical scrape (2014-2024): ~10-20 minutes
- Single year: ~1-3 minutes
- Data size: ~500-1000 rankings per year

## Legal and Ethical Use

This scraper:
- Only accesses publicly available data
- Includes delays to be respectful to the website
- Does not overwhelm the server with requests
- Is intended for research and analysis purposes

Please use responsibly and in accordance with the website's terms of service.
