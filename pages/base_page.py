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
        # Menggunakan Config.EXPLICIT_WAIT untuk semua waits
        self.wait = WebDriverWait(driver, Config.EXPLICIT_WAIT) 
        self.actions = ActionChains(driver)
    
    def find_element(self, locator, by=By.CSS_SELECTOR, timeout=None):
            """Find element dengan wait sampai element terlihat (visibility_of_element_located)"""
            try:
                wait_time = timeout if timeout else Config.EXPLICIT_WAIT
                wait = WebDriverWait(self.driver, wait_time)
                # Menggunakan visibility_of_element_located
                return wait.until(EC.visibility_of_element_located((by, locator))) 
            except TimeoutException:
                # Mengganti exception agar lebih jelas
                raise Exception(f"Element tidak ditemukan (Timeout): {locator} menggunakan {by}")
        
    def find_elements(self, locator, by=By.CSS_SELECTOR):
        """Find multiple elements"""
        return self.driver.find_elements(by, locator)
    
    def wait_for_element_clickable(self, locator, by=By.CSS_SELECTOR):
        """Wait sampai element clickable (EC.element_to_be_clickable)"""
        return self.wait.until(EC.element_to_be_clickable((by, locator)))

    def click(self, locator, by=By.CSS_SELECTOR):
        """Click element setelah dipastikan clickable"""
        element = self.wait_for_element_clickable(locator, by)
        element.click()
    
    # 💥 FUNGSI BARU UNTUK MENGATASI TIMEOUT PADA TOMBOL (FORCE CLICK) 💥
    def force_click(self, locator, by=By.CSS_SELECTOR):
        """Klik element menggunakan JavaScript (mengatasi masalah overlay/interactability)"""
        # Tunggu elemen sampai clickable (seperti di fungsi click normal)
        element = self.wait_for_element_clickable(locator, by) 
        # Lakukan klik menggunakan JavaScript
        self.driver.execute_script("arguments[0].click();", element)
    
    def input_text(self, locator, text, by=By.CSS_SELECTOR, clear=True, timeout=10): # <-- Tambahkan 'by' dan 'clear'
        """Input text ke field"""
        try:
            # Panggil find_element Anda yang sudah benar
            element = self.find_element(locator, by=by, timeout=timeout) 
            
            if clear:
                element.clear()
            element.send_keys(text)
        except TimeoutException:
            raise Exception(f"Element tidak ditemukan: {locator} (Timeout setelah {timeout}s)")
                
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
    
    # ... (Fungsi-fungsi lain tetap sama seperti sebelumnya) ...
    # ...
    
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
    def _get_locator_tuple(self, locator, by_method=By.CSS_SELECTOR):
            if isinstance(locator, tuple):
                return locator
            return (by_method, locator) # Asumsi locator yang masuk adalah string CSS/XPATH

    # def input_text(self, locator, text, by_method=By.CSS_SELECTOR, timeout=10):
    #     try:
    #         locator_tuple = self._get_locator_tuple(locator, by_method)
    #         # WAJIB: Gunakan Explicit Wait untuk Visibility sebelum Send Keys
    #         element = WebDriverWait(self.driver, timeout).until(
    #             EC.visibility_of_element_located(locator_tuple)
    #         )
    #         element.clear() # Disarankan untuk membersihkan field
    #         element.send_keys(text)
    #     except TimeoutException:
    #         raise Exception(f"Element tidak ditemukan: {locator} (Timeout setelah {timeout}s)")