import pytest
from pages.login_page import LoginPage # <-- Asumsi path ke LoginPage
from pages.login_page import LoginPageLocators
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from webdriver_manager.firefox import GeckoDriverManager
from config.config import Config
from selenium.webdriver.support.ui import WebDriverWait
from pages.login_page import LoginPageLocators
from utils.helpers import ScreenshotHelper
import os

@pytest.fixture(scope="session")
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
    driver.implicitly_wait(0)
    driver.set_page_load_timeout(Config.PAGE_LOAD_TIMEOUT)
    driver.maximize_window()
    
    # Navigate to base URL
    driver.get(Config.BASE_URL)
    
    yield driver
    
    # Teardown
    # Take screenshot on failure
    if hasattr(request.node, 'rep_call') and request.node.rep_call.failed:
        test_name = request.node.name
        # Pastikan ScreenshotHelper sudah diimpor dan berfungsi
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

@pytest.fixture(scope="function")
def login_admin(driver):
    """Fixture untuk login sebagai admin sebelum menjalankan tes."""
    driver.get(f"{Config.BASE_URL}/login")

    # Asumsi: Anda memiliki class LoginPage dan method login
    login_page = LoginPage(driver) 
    
    print(f"DEBUG: URL sebelum login: {driver.current_url}")
    
    # Navigasi ke halaman login (jika belum di sana dari driver.get(Config.BASE_URL))
   
    try:
    # 20 detik untuk tombol Login (menggunakan WebDriverWait dari LoginPage)
        LoginPage(driver).wait.until(
            EC.presence_of_element_located((By.CSS_SELECTOR, LoginPageLocators.LOGIN_BUTTON)) 
        )
        print("[INFO] Tombol Login terdeteksi di DOM.")
    except TimeoutException:
        print("[WARNING] Tombol Login tidak terdeteksi di DOM setelah 20s. Melanjutkan...")

    login_page.wait_for_login_form_load()
    try:
    # Lakukan Login
        login_page.login(
            email=Config.ADMIN_EMAIL,
            password=Config.ADMIN_PASSWORD
        )

    except Exception as e:
        # Menangkap error spesifik dari input email
        print(f"DEBUG ERROR: URL saat kegagalan input email: {driver.current_url}")
        # Cetak screenshot atau HTML untuk analisis offline
        # driver.get_screenshot_as_file("error_login.png")
        raise Exception(f"Login Gagal. URL: {driver.current_url}. Original Error: {e}")
    
    # WAJIB: Tambahkan Wait untuk memastikan login berhasil dan navigasi selesai
    # login_page.wait_for_successful_admin_login() 
    login_page.wait_for_successful_admin_login() # Panggil method wait yang baru

    yield driver