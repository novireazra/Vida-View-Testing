import random
import string
from datetime import datetime, timedelta
from faker import Faker
import time

fake = Faker('id_ID')  # Indonesian locale

class TestDataGenerator:
    @staticmethod
    def generate_random_email(prefix="test"):
        """Generate random email"""
        timestamp = int(time.time())
        return f"{prefix}_{timestamp}@test.com"
    
    @staticmethod
    def generate_random_username(prefix="user"):
        """Generate random username"""
        random_str = ''.join(random.choices(string.ascii_lowercase + string.digits, k=6))
        return f"{prefix}_{random_str}"
    
    @staticmethod
    def generate_random_phone():
        """Generate random Indonesian phone"""
        return f"08{random.randint(1000000000, 9999999999)}"
    
    @staticmethod
    def generate_random_full_name():
        """Generate random Indonesian full name"""
        return fake.name()
    
    @staticmethod
    def generate_random_address():
        """Generate random Indonesian address"""
        return fake.address()
    
    @staticmethod
    def generate_birth_date(age=25):
        """Generate birth date (must be 18+)"""
        today = datetime.now()
        birth_date = today - timedelta(days=age*365)
        return birth_date.strftime("%Y-%m-%d")
    
    @staticmethod
    def generate_future_date(days_ahead=7):
        """Generate future date"""
        future = datetime.now() + timedelta(days=days_ahead)
        return future.strftime("%Y-%m-%d")
    
    @staticmethod
    def generate_booking_dates(months=6):
        """Generate booking start and end dates"""
        start = datetime.now() + timedelta(days=7)
        end = start + timedelta(days=months*30)
        return start.strftime("%Y-%m-%d"), end.strftime("%Y-%m-%d")
    
    @staticmethod
    def generate_promo_code(prefix="PROMO"):
        """Generate random promo code"""
        random_str = ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))
        return f"{prefix}{random_str}"
    
    @staticmethod
    def generate_transaction_id():
        """Generate random transaction ID"""
        timestamp = int(time.time())
        random_num = random.randint(1000, 9999)
        return f"TRX{timestamp}{random_num}"

class WaitHelper:
    @staticmethod
    def wait_for_toast(driver, timeout=5):
        """Wait for toast notification to appear and disappear"""
        from selenium.webdriver.support.ui import WebDriverWait
        from selenium.webdriver.support import expected_conditions as EC
        from selenium.webdriver.common.by import By
        
        try:
            # Wait for toast to appear
            WebDriverWait(driver, timeout).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, ".Toastify__toast"))
            )
            time.sleep(1)
            # Wait for toast to disappear
            WebDriverWait(driver, timeout).until_not(
                EC.presence_of_element_located((By.CSS_SELECTOR, ".Toastify__toast"))
            )
        except:
            pass
    
    @staticmethod
    def wait_for_modal(driver, timeout=5):
        """Wait for modal to open"""
        from selenium.webdriver.support.ui import WebDriverWait
        from selenium.webdriver.support import expected_conditions as EC
        from selenium.webdriver.common.by import By
        
        WebDriverWait(driver, timeout).until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, ".fixed.inset-0"))
        )
        time.sleep(0.5)

class ScreenshotHelper:
    @staticmethod
    def take_screenshot_on_failure(driver, test_name):
        """Take screenshot on test failure"""
        from config.config import Config
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"{test_name}_{timestamp}.png"
        filepath = Config.SCREENSHOTS_DIR / filename
        driver.save_screenshot(str(filepath))
        return str(filepath)