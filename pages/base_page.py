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
    
    def find_element(self, locator, by=By.CSS_SELECTOR, timeout=None):
        """Find element dengan wait"""
        try:
            wait_time = timeout if timeout else Config.EXPLICIT_WAIT
            wait = WebDriverWait(self.driver, wait_time)
            return wait.until(EC.presence_of_element_located((by, locator)))
        except TimeoutException:
            raise Exception(f"Element tidak ditemukan: {locator}")
    
    def find_elements(self, locator, by=By.CSS_SELECTOR):
        """Find multiple elements"""
        return self.driver.find_elements(by, locator)
    
    def click(self, locator, by=By.CSS_SELECTOR):
        """Click element"""
        element = self.find_element(locator, by)
        element.click()
    
    def input_text(self, locator, text, by=By.CSS_SELECTOR, clear=True):
        """Input text ke field"""
        element = self.find_element(locator, by)
        if clear:
            element.clear()
        element.send_keys(text)
    
    def get_text(self, locator, by=By.CSS_SELECTOR):
        """Get text dari element"""
        element = self.find_element(locator, by)
        return element.text
    
    def is_element_visible(self, locator, by=By.CSS_SELECTOR, timeout=5):
        """Check apakah element visible"""
        try:
            wait = WebDriverWait(self.driver, timeout)
            wait.until(EC.visibility_of_element_located((by, locator)))
            return True
        except TimeoutException:
            return False
    
    def is_element_present(self, locator, by=By.CSS_SELECTOR):
        """Check apakah element ada di DOM"""
        try:
            self.driver.find_element(by, locator)
            return True
        except NoSuchElementException:
            return False
    
    def wait_for_element_clickable(self, locator, by=By.CSS_SELECTOR):
        """Wait sampai element clickable"""
        return self.wait.until(EC.element_to_be_clickable((by, locator)))
    
    def scroll_to_element(self, locator, by=By.CSS_SELECTOR):
        """Scroll ke element"""
        element = self.find_element(locator, by)
        self.driver.execute_script("arguments[0].scrollIntoView(true);", element)
        time.sleep(0.5)
    
    def take_screenshot(self, filename):
        """Take screenshot"""
        filepath = Config.SCREENSHOTS_DIR / filename
        self.driver.save_screenshot(str(filepath))
        return str(filepath)
    
    def get_current_url(self):
        """Get current URL"""
        return self.driver.current_url
    
    def navigate_to(self, url):
        """Navigate to URL"""
        self.driver.get(url)
    
    def refresh_page(self):
        """Refresh halaman"""
        self.driver.refresh()
    
    def get_page_title(self):
        """Get page title"""
        return self.driver.title
    
    def switch_to_alert(self):
        """Switch to alert"""
        return self.wait.until(EC.alert_is_present())
    
    def accept_alert(self):
        """Accept alert"""
        alert = self.switch_to_alert()
        alert.accept()
    
    def dismiss_alert(self):
        """Dismiss alert"""
        alert = self.switch_to_alert()
        alert.dismiss()
    
    def select_dropdown_by_text(self, locator, text, by=By.CSS_SELECTOR):
        """Select dropdown by visible text"""
        from selenium.webdriver.support.select import Select
        element = self.find_element(locator, by)
        select = Select(element)
        select.select_by_visible_text(text)
    
    def select_dropdown_by_value(self, locator, value, by=By.CSS_SELECTOR):
        """Select dropdown by value"""
        from selenium.webdriver.support.select import Select
        element = self.find_element(locator, by)
        select = Select(element)
        select.select_by_value(value)
    
    def upload_file(self, locator, filepath, by=By.CSS_SELECTOR):
        """Upload file"""
        element = self.find_element(locator, by)
        element.send_keys(str(filepath))
    
    def hover_element(self, locator, by=By.CSS_SELECTOR):
        """Hover over element"""
        element = self.find_element(locator, by)
        self.actions.move_to_element(element).perform()
    
    def wait_for_page_load(self, timeout=30):
        """Wait for page load"""
        WebDriverWait(self.driver, timeout).until(
            lambda driver: driver.execute_script("return document.readyState") == "complete"
        )