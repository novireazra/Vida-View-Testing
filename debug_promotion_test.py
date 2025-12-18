"""
Debug script untuk test promotion creation
"""
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from config.config import Config

# Setup
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
driver.maximize_window()

try:
    print("=" * 80)
    print("DEBUG: PROMOTION CREATION TEST")
    print("=" * 80)

    # 1. Login sebagai admin
    print("\n1. Login sebagai admin...")
    driver.get(f"{Config.BASE_URL}/login")
    time.sleep(2)

    email_input = driver.find_element(By.NAME, "email")
    password_input = driver.find_element(By.NAME, "password")
    email_input.send_keys(Config.ADMIN_EMAIL)
    password_input.send_keys(Config.ADMIN_PASSWORD)

    login_btn = driver.find_element(By.CSS_SELECTOR, "button[type='submit']")
    login_btn.click()
    time.sleep(3)

    print(f"   Current URL after login: {driver.current_url}")

    # 2. Navigate to promotions
    print("\n2. Navigating to promotions page...")
    driver.get(f"{Config.BASE_URL}/admin/promotions")
    time.sleep(3)

    print(f"   Current URL: {driver.current_url}")

    # 3. Check for "Tambah Promosi" button
    print("\n3. Looking for 'Tambah Promosi' button...")
    try:
        add_btn = driver.find_element(By.XPATH, "//button[contains(., 'Tambah Promosi')]")
        print(f"   ✅ Found button: {add_btn.text}")
        print(f"   Button visible: {add_btn.is_displayed()}")
        print(f"   Button enabled: {add_btn.is_enabled()}")
    except Exception as e:
        print(f"   ❌ Button not found: {e}")

        # Try to find all buttons
        all_buttons = driver.find_elements(By.TAG_NAME, "button")
        print(f"\n   Found {len(all_buttons)} buttons on page:")
        for i, btn in enumerate(all_buttons[:10]):  # First 10 buttons
            print(f"   Button {i+1}: '{btn.text}' (visible: {btn.is_displayed()})")

        driver.save_screenshot("debug_no_add_button.png")
        raise

    # 4. Click "Tambah Promosi" button
    print("\n4. Clicking 'Tambah Promosi' button...")
    add_btn.click()
    time.sleep(2)

    # 5. Check if modal opened
    print("\n5. Checking if modal opened...")
    try:
        # Try different ways to find inputs
        print("   Trying to find code input by placeholder...")
        code_input = driver.find_element(By.CSS_SELECTOR, "input[placeholder*='LEBARAN']")
        print(f"   ✅ Found code input: visible={code_input.is_displayed()}")
    except:
        print("   ❌ Code input not found by placeholder 'LEBARAN'")

        # Try finding all inputs
        all_inputs = driver.find_elements(By.TAG_NAME, "input")
        print(f"\n   Found {len(all_inputs)} inputs:")
        for i, inp in enumerate(all_inputs):
            placeholder = inp.get_attribute("placeholder")
            input_type = inp.get_attribute("type")
            visible = inp.is_displayed()
            print(f"   Input {i+1}: type='{input_type}', placeholder='{placeholder}', visible={visible}")

        driver.save_screenshot("debug_modal_inputs.png")
        raise

    # 6. Fill form
    print("\n6. Filling form...")

    # Code
    print("   Filling code...")
    code_input.clear()
    code_input.send_keys("DEBUG2024")
    print(f"   Code value: {code_input.get_attribute('value')}")

    # Title
    print("   Filling title...")
    title_input = driver.find_element(By.CSS_SELECTOR, "input[placeholder*='Diskon']")
    title_input.clear()
    title_input.send_keys("Debug Test Promo")
    print(f"   Title value: {title_input.get_attribute('value')}")

    # Type
    print("   Selecting type...")
    type_select = driver.find_element(By.CSS_SELECTOR, "select")
    print(f"   Select options: {[opt.text for opt in type_select.find_elements(By.TAG_NAME, 'option')]}")
    type_select.find_element(By.CSS_SELECTOR, "option[value='percent']").click()

    # Value
    print("   Filling value...")
    value_inputs = driver.find_elements(By.CSS_SELECTOR, "input[type='number']")
    print(f"   Found {len(value_inputs)} number inputs")
    value_inputs[0].clear()
    value_inputs[0].send_keys("15")
    print(f"   Value: {value_inputs[0].get_attribute('value')}")

    # Dates
    print("   Filling dates...")
    date_inputs = driver.find_elements(By.CSS_SELECTOR, "input[type='date']")
    print(f"   Found {len(date_inputs)} date inputs")

    if len(date_inputs) >= 2:
        date_inputs[0].send_keys("01012024")
        print(f"   Start date: {date_inputs[0].get_attribute('value')}")

        date_inputs[1].send_keys("31012024")
        print(f"   End date: {date_inputs[1].get_attribute('value')}")
    else:
        print(f"   ❌ Not enough date inputs found!")

    # 7. Find submit button
    print("\n7. Looking for submit button...")
    submit_buttons = driver.find_elements(By.XPATH, "//button[@type='submit']")
    print(f"   Found {len(submit_buttons)} submit buttons")

    for i, btn in enumerate(submit_buttons):
        print(f"   Submit button {i+1}: '{btn.text}', visible={btn.is_displayed()}")

    # Try to find by text
    tambah_buttons = driver.find_elements(By.XPATH, "//button[contains(text(), 'Tambah')]")
    print(f"   Found {len(tambah_buttons)} buttons with 'Tambah' text")

    for i, btn in enumerate(tambah_buttons):
        print(f"   Tambah button {i+1}: '{btn.text}', visible={btn.is_displayed()}, type={btn.get_attribute('type')}")

    driver.save_screenshot("debug_before_submit.png")

    print("\n8. Ready to submit. Pausing for manual inspection...")
    input("Press Enter to submit form (or Ctrl+C to cancel)...")

    # Submit
    if submit_buttons:
        submit_buttons[-1].click()  # Click last submit button (in modal)
        time.sleep(3)
        print("   Form submitted!")

        driver.save_screenshot("debug_after_submit.png")

        # Check if success
        promo_cards = driver.find_elements(By.CSS_SELECTOR, ".bg-white.rounded-xl.shadow-md")
        print(f"\n   Found {len(promo_cards)} promotion cards after submit")

except Exception as e:
    print(f"\n❌ ERROR: {e}")
    import traceback
    traceback.print_exc()
    driver.save_screenshot("debug_error.png")

finally:
    print("\n" + "=" * 80)
    print("Debug completed. Check screenshots folder.")
    print("=" * 80)
    input("Press Enter to close browser...")
    driver.quit()
