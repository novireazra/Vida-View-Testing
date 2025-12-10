import pytest
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.firefox import GeckoDriverManager
from config.config import Config
from utils.helpers import ScreenshotHelper
import os

@pytest.fixture(scope="function")
def driver(request):
    """Setup WebDriver"""
    
    # Browser configuration
    if Config.BROWSER.lower() == "chrome":
        chrome_options = ChromeOptions()
        if Config.HEADLESS:
            chrome_options.add_argument("--headless")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument("--window-size=1920,1080")
        chrome_options.add_argument("--disable-blink-features=AutomationControlled")
        chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
        chrome_options.add_experimental_option('useAutomationExtension', False)
        
        # Install chromedriver and ensure correct path
        driver_path = ChromeDriverManager().install()
        # Fix for webdriver_manager issue with Chrome for Testing
        if os.path.isdir(driver_path):
            driver_path = os.path.join(driver_path, "chromedriver")
        elif not driver_path.endswith("chromedriver"):
            # If path points to wrong file, find the actual chromedriver
            driver_dir = os.path.dirname(driver_path)
            chromedriver_path = os.path.join(driver_dir, "chromedriver")
            if os.path.exists(chromedriver_path):
                driver_path = chromedriver_path

        service = Service(driver_path)
        driver = webdriver.Chrome(service=service, options=chrome_options)
    
    elif Config.BROWSER.lower() == "firefox":
        firefox_options = FirefoxOptions()
        if Config.HEADLESS:
            firefox_options.add_argument("--headless")
        
        service = Service(GeckoDriverManager().install())
        driver = webdriver.Firefox(service=service, options=firefox_options)
    
    else:
        raise ValueError(f"Browser {Config.BROWSER} tidak didukung")
    
    # Set timeouts
    driver.implicitly_wait(Config.IMPLICIT_WAIT)
    driver.set_page_load_timeout(Config.PAGE_LOAD_TIMEOUT)
    driver.maximize_window()
    
    # Navigate to base URL
    driver.get(Config.BASE_URL)
    
    yield driver
    
    # Teardown
    # Take screenshot on failure
    if request.node.rep_call.failed:
        test_name = request.node.name
        ScreenshotHelper.take_screenshot_on_failure(driver, test_name)
    
    driver.quit()

@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """Hook untuk capture test result"""
    outcome = yield
    rep = outcome.get_result()
    setattr(item, f"rep_{rep.when}", rep)

@pytest.fixture(scope="session")
def create_test_files():
    """Create test files untuk upload"""
    import shutil
    from PIL import Image
    
    # Create sample KTP image
    ktp_image = Image.new('RGB', (800, 500), color='white')
    ktp_image.save(Config.KTP_IMAGE)
    
    # Create sample Selfie image
    selfie_image = Image.new('RGB', (600, 800), color='white')
    selfie_image.save(Config.SELFIE_IMAGE)
    
    # Create sample PDF
    from reportlab.pdfgen import canvas
    c = canvas.Canvas(str(Config.INCOME_PROOF))
    c.drawString(100, 750, "Sample Income Proof Document")
    c.save()
    
    yield
    
    # Cleanup (optional)
    # os.remove(Config.KTP_IMAGE)
    # os.remove(Config.SELFIE_IMAGE)
    # os.remove(Config.INCOME_PROOF)