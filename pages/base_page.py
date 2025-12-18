from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from config.config import Config
import time

class BasePage:
    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, Config.EXPLICIT_WAIT) 
        self.actions = ActionChains(driver)

    def _parse_locator(self, locator, by_default):
        """Internal helper untuk memisahkan tuple atau string locator"""
        if isinstance(locator, tuple):
            return locator # Mengembalikan (By.STRATEGY, "selector")
        return (by_default, locator)

    def find_element(self, locator, by=By.CSS_SELECTOR, timeout=None):
        """Smart Find: Mendukung Tuple atau String"""
        try:
            loc_tuple = self._parse_locator(locator, by)
            wait_time = timeout if timeout else Config.EXPLICIT_WAIT
            wait = WebDriverWait(self.driver, wait_time)
            return wait.until(EC.visibility_of_element_located(loc_tuple)) 
        except TimeoutException:
            raise Exception(f"Element tidak ditemukan (Timeout): {locator}")

    def find_elements(self, locator, by=By.CSS_SELECTOR):
        loc_tuple = self._parse_locator(locator, by)
        return self.driver.find_elements(*loc_tuple)

    def wait_for_element_clickable(self, locator, by=By.CSS_SELECTOR):
        loc_tuple = self._parse_locator(locator, by)
        return self.wait.until(EC.element_to_be_clickable(loc_tuple))

    def click(self, locator, by=By.CSS_SELECTOR):
        element = self.wait_for_element_clickable(locator, by)
        element.click()

    def force_click(self, locator, by=By.CSS_SELECTOR):
        """Klik menggunakan JavaScript"""
        element = self.wait_for_element_clickable(locator, by) 
        self.driver.execute_script("arguments[0].click();", element)

    def input_text(self, locator, text, by=By.CSS_SELECTOR, clear=True, timeout=10):
        try:
            element = self.find_element(locator, by=by, timeout=timeout) 
            if clear:
                element.clear()
            element.send_keys(text)
        except Exception as e:
            raise Exception(f"Gagal input text pada {locator}: {str(e)}")
                
    def get_text(self, locator, by=By.CSS_SELECTOR):
        element = self.find_element(locator, by)
        return element.text

    def is_element_visible(self, locator, by=By.CSS_SELECTOR, timeout=5):
        try:
            loc_tuple = self._parse_locator(locator, by)
            wait = WebDriverWait(self.driver, timeout)
            wait.until(EC.visibility_of_element_located(loc_tuple))
            return True
        except TimeoutException:
            return False

    def is_element_present(self, locator, by=By.CSS_SELECTOR):
        loc_tuple = self._parse_locator(locator, by)
        try:
            self.driver.find_element(*loc_tuple)
            return True
        except NoSuchElementException:
            return False

    def scroll_to_element(self, locator, by=By.CSS_SELECTOR):
        element = self.find_element(locator, by)
        self.driver.execute_script("arguments[0].scrollIntoView(true);", element)
        time.sleep(0.5)

    def take_screenshot(self, filename):
        filepath = Config.SCREENSHOTS_DIR / filename
        self.driver.save_screenshot(str(filepath))
        return str(filepath)

    def navigate_to(self, url):
        self.driver.get(url)

    def wait_for_page_load(self, timeout=30):
        WebDriverWait(self.driver, timeout).until(
            lambda driver: driver.execute_script("return document.readyState") == "complete"
        )

    def select_dropdown_by_text(self, locator, text, by=By.CSS_SELECTOR):
        from selenium.webdriver.support.select import Select
        element = self.find_element(locator, by)
        Select(element).select_by_visible_text(text)

    def upload_file(self, locator, filepath, by=By.CSS_SELECTOR):
        loc_tuple = self._parse_locator(locator, by)
        element = self.driver.find_element(*loc_tuple)
        element.send_keys(str(filepath))
    
    def refresh_page(self):
        """Refresh halaman browser"""
        self.driver.refresh()
        self.wait_for_page_load()

    def get_current_url(self):
        """Mengambil URL saat ini"""
        return self.driver.current_url