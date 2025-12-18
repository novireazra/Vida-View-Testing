"""
Quick debug script to test apartment navigation
"""
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

# Setup
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
driver.maximize_window()

try:
    # Navigate to apartments page
    print("1. Navigating to apartments page...")
    driver.get("http://localhost:3000/apartments")
    time.sleep(3)

    print(f"   Current URL: {driver.current_url}")

    # Try old locator
    print("\n2. Testing OLD locator (.bg-white.rounded-lg.shadow-md)...")
    old_cards = driver.find_elements(By.CSS_SELECTOR, ".bg-white.rounded-lg.shadow-md")
    print(f"   Found {len(old_cards)} elements with old locator")

    # Try new locator
    print("\n3. Testing NEW locator (a[href^='/apartments/'])...")
    new_cards = driver.find_elements(By.CSS_SELECTOR, "a[href^='/apartments/']")
    print(f"   Found {len(new_cards)} elements with new locator")

    if new_cards:
        print(f"   First card href: {new_cards[0].get_attribute('href')}")
        print(f"   First card text preview: {new_cards[0].text[:100]}...")

        # Try clicking
        print("\n4. Trying to click first apartment card...")
        first_card = new_cards[0]

        # Scroll into view
        driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", first_card)
        time.sleep(1)

        # Click
        first_card.click()
        time.sleep(3)

        print(f"   After click, URL: {driver.current_url}")

        if "/apartments/" in driver.current_url and not driver.current_url.endswith("/apartments"):
            print("   ✅ SUCCESS! Navigation to detail page worked!")
        else:
            print("   ❌ FAILED! Still on apartments list page")
    else:
        print("   ❌ No apartment cards found!")

    # Check for specific apartment grid structure
    print("\n5. Checking grid structure...")
    grids = driver.find_elements(By.CSS_SELECTOR, ".grid")
    print(f"   Found {len(grids)} grid elements")

    for i, grid in enumerate(grids):
        links = grid.find_elements(By.CSS_SELECTOR, "a[href^='/apartments/']")
        print(f"   Grid {i+1}: {len(links)} apartment links")

finally:
    print("\n6. Cleaning up...")
    input("Press Enter to close browser...")
    driver.quit()
