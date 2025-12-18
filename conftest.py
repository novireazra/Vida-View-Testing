import pytest
import os
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

from config.config import Config
from pages.login_page import LoginPage
from utils.helpers import ScreenshotHelper


# =========================
# WEB DRIVER FIXTURE
# =========================
@pytest.fixture(scope="session")
def driver(request):
    """
    Setup WebDriver dengan Selenium Manager (Selenium 4.6+)
    + Support download (Chrome)
    """
    driver = None
    browser_name = Config.BROWSER.lower()

    if browser_name == "chrome":
        chrome_options = ChromeOptions()

        if Config.HEADLESS:
            chrome_options.add_argument("--headless=new")

        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument("--window-size=1920,1080")
        chrome_options.add_argument("--disable-blink-features=AutomationControlled")

        chrome_options.add_experimental_option(
            "excludeSwitches", ["enable-automation"]
        )
        chrome_options.add_experimental_option(
            "useAutomationExtension", False
        )

        # ===== DOWNLOAD CONFIG (WAJIB UNTUK EXPORT TEST) =====
        download_dir = os.path.join(os.getcwd(), "downloads")
        os.makedirs(download_dir, exist_ok=True)

        prefs = {
            "download.default_directory": download_dir,
            "download.prompt_for_download": False,
            "download.directory_upgrade": True,
            "safebrowsing.enabled": True
        }
        chrome_options.add_experimental_option("prefs", prefs)

        driver = webdriver.Chrome(options=chrome_options)

    elif browser_name == "firefox":
        pytest.skip("Firefox belum didukung untuk test export (download dialog OS).")

    else:
        raise ValueError(f"Browser '{browser_name}' tidak didukung.")

    driver.set_page_load_timeout(Config.PAGE_LOAD_TIMEOUT)
    driver.maximize_window()
    driver.get(Config.BASE_URL)

    yield driver

    # ===== SCREENSHOT JIKA TEST FAIL =====
    if hasattr(request.node, "rep_call") and request.node.rep_call.failed:
        try:
            ScreenshotHelper.take_screenshot_on_failure(
                driver, request.node.name
            )
        except Exception as e:
            print(f"Gagal mengambil screenshot: {e}")

    driver.quit()


# =========================
# PYTEST REPORT HOOK
# =========================
@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    rep = outcome.get_result()
    setattr(item, f"rep_{rep.when}", rep)


# =========================
# FILE DUMMY FIXTURE
# =========================
@pytest.fixture(scope="session")
def create_test_files():
    """
    Membuat file dummy untuk upload (KTP, Selfie, PDF)
    """
    from PIL import Image
    from reportlab.pdfgen import canvas

    os.makedirs(os.path.dirname(Config.KTP_IMAGE), exist_ok=True)

    Image.new("RGB", (800, 500), "white").save(Config.KTP_IMAGE)
    Image.new("RGB", (600, 800), "white").save(Config.SELFIE_IMAGE)

    c = canvas.Canvas(str(Config.INCOME_PROOF))
    c.drawString(100, 750, "Sample Income Proof Document")
    c.save()

    yield


# =========================
# LOGIN ADMIN FIXTURE (AMAN)
# =========================
@pytest.fixture(scope="function")
def login_admin(driver):
    """
    Fixture login admin yang:
    - Aman dipanggil berkali-kali
    - Tidak double login
    - Tidak bergantung state sebelumnya
    """
    login_page = LoginPage(driver)

    try:
        login_page.navigate_to_login()

        if login_page.is_login_form_visible():
            login_page.login(
                email=Config.ADMIN_EMAIL,
                password=Config.ADMIN_PASSWORD
            )
            login_page.wait_for_successful_admin_login()
        else:
            print("[INFO] Admin sudah login, lewati proses login.")

    except Exception as e:
        pytest.fail(f"Login Admin Gagal: {str(e)}")

    yield driver
