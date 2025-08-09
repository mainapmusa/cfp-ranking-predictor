#!/usr/bin/env python3
"""
ChromeDriver Fix Script

This script helps resolve ChromeDriver installation issues.
"""

import os
import shutil
import subprocess
import sys
from pathlib import Path

def check_chrome_installed():
    """Check if Chrome browser is installed."""
    chrome_paths = [
        "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",
        "/Applications/Chrome.app/Contents/MacOS/Chrome",
    ]
    
    for path in chrome_paths:
        if os.path.exists(path):
            print(f"✅ Chrome found at: {path}")
            return True
    
    print("❌ Chrome browser not found. Please install Google Chrome first.")
    return False

def clear_webdriver_cache():
    """Clear webdriver-manager cache."""
    cache_dir = Path.home() / ".wdm"
    if cache_dir.exists():
        print(f"🧹 Clearing webdriver cache: {cache_dir}")
        shutil.rmtree(cache_dir)
        print("✅ Cache cleared")
    else:
        print("ℹ️  No webdriver cache found")

def install_chromedriver_homebrew():
    """Try to install ChromeDriver via Homebrew."""
    try:
        print("🍺 Trying to install ChromeDriver via Homebrew...")
        
        # Check if brew is installed
        result = subprocess.run(["which", "brew"], capture_output=True, text=True)
        if result.returncode != 0:
            print("❌ Homebrew not found. Install from https://brew.sh")
            return False
        
        # Install chromedriver
        result = subprocess.run(["brew", "install", "chromedriver"], capture_output=True, text=True)
        if result.returncode == 0:
            print("✅ ChromeDriver installed via Homebrew")
            return True
        else:
            print(f"❌ Homebrew install failed: {result.stderr}")
            return False
            
    except Exception as e:
        print(f"❌ Homebrew install error: {e}")
        return False

def test_chromedriver():
    """Test if ChromeDriver works."""
    try:
        print("🧪 Testing ChromeDriver installation...")
        
        from selenium import webdriver
        from selenium.webdriver.chrome.options import Options
        
        chrome_options = Options()
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        
        driver = webdriver.Chrome(options=chrome_options)
        driver.get("https://www.google.com")
        print(f"✅ ChromeDriver test successful! Page title: {driver.title}")
        driver.quit()
        return True
        
    except Exception as e:
        print(f"❌ ChromeDriver test failed: {e}")
        return False

def main():
    """Main fix function."""
    print("ChromeDriver Fix Script")
    print("=" * 50)
    
    # Step 1: Check Chrome
    if not check_chrome_installed():
        print("\n📋 Action needed: Install Google Chrome browser")
        print("   Download from: https://www.google.com/chrome/")
        return
    
    # Step 2: Clear cache
    clear_webdriver_cache()
    
    # Step 3: Try Homebrew install
    homebrew_success = install_chromedriver_homebrew()
    
    # Step 4: Test ChromeDriver
    if test_chromedriver():
        print("\n🎉 ChromeDriver is working! You can now run the scraper.")
        print("   Run: python run_scraper.py")
    else:
        print("\n❌ ChromeDriver still not working. Manual steps:")
        print("\n1. Update Chrome to the latest version")
        print("2. Try manual ChromeDriver download:")
        print("   - Go to: https://chromedriver.chromium.org/")
        print("   - Download version matching your Chrome")
        print("   - Extract to /usr/local/bin/chromedriver")
        print("   - Run: chmod +x /usr/local/bin/chromedriver")
        print("\n3. Alternative: Use different browser driver")
        print("   - Install Firefox and use geckodriver")
        print("   - pip install geckodriver-autoinstaller")

if __name__ == "__main__":
    main()
