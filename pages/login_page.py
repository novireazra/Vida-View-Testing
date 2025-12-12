from pages.base_page import BasePage
from config.locators import LoginPageLocators, AdminDashboardLocators
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException # <--- HARUS ADA
class LoginPage(BasePage):
    def __init__(self, driver):
        super().__init__(driver)
        self.locators = LoginPageLocators()
    
    def navigate_to_login(self):
        """Navigate ke halaman login"""
        from config.config import Config
        self.navigate_to(f"{Config.BASE_URL}/login")
        self.wait_for_page_load()
    
    def input_email(self, email):
        """Input email"""
        # WAJIB: Tentukan By.XPATH karena Anda menggunakan locator XPATH
        self.input_text(self.locators.EMAIL_INPUT, email, by=By.XPATH)
        
    def input_password(self, password):
        """Input password"""
        # Jika PASSWORD_INPUT masih CSS:
        self.input_text(self.locators.PASSWORD_INPUT, password, by=By.CSS_SELECTOR)
        # Jika PASSWORD_INPUT juga XPATH, gunakan:
        # self.input_text(self.locators.PASSWORD_INPUT, password, by=By.XPATH)
        
    def click_login_button(self):
        """Click login button"""
        self.click(self.locators.LOGIN_BUTTON)
    
    def check_remember_me(self):
        """Check remember me checkbox"""
        self.click(self.locators.REMEMBER_CHECKBOX)
    
    def click_register_link(self):
        """Click register link"""
        self.click(self.locators.REGISTER_LINK)
    
    def is_error_displayed(self):
        """Check apakah error message ditampilkan"""
        return self.is_element_visible(self.locators.ERROR_MESSAGE, timeout=3)
    
    def get_error_message(self):
        """Get error message text"""
        return self.get_text(self.locators.ERROR_MESSAGE)
            
    def login(self, email, password, remember=False):
        """Complete login flow"""
        self.input_email(email)
        self.input_password(password)
        if remember:
            self.check_remember_me()
        self.click_login_button()
    
    def wait_for_login_form_load(self):
        """Menunggu elemen input email terlihat. Termasuk refresh jika timeout."""
        TIMEOUT_INITIAL = 15
        locator = self.locators.EMAIL_INPUT # Ambil locator email
        
        try:
            self.wait_for_page_load() 
            # Perhatikan: Pastikan find_element di BasePage menerima 'timeout'
            self.find_element(locator, By.CSS_SELECTOR, timeout=TIMEOUT_INITIAL) 

            print("[INFO] Halaman Login termuat, form email terlihat.")

        except TimeoutException:
            print(f"[ERROR] Timeout saat menunggu form login (Percobaan 1, {TIMEOUT_INITIAL}s). URL: {self.driver.current_url}")
            
            # Fallback: Refresh halaman dan coba lagi
            self.driver.refresh()
            self.wait_for_page_load()

            TIMEOUT_REFRESH = 10
            try:
                self.find_element(locator, By.CSS_SELECTOR, timeout=TIMEOUT_REFRESH)
                print("[INFO] Elemen email terlihat setelah refresh.")
            except TimeoutException:
                # Gagal total setelah refresh
                raise Exception(f"Element tidak ditemukan: {locator} setelah refresh ({TIMEOUT_REFRESH}s). Halaman gagal dimuat secara konsisten.")
    
    def wait_for_successful_admin_login(self):
            """
            Menunggu elemen Admin Dashboard (misalnya, link Users) muncul setelah login berhasil.
            """
            # AdminDashboardLocators.USERS_LINK = "a[href='/admin/users']"
            try:
                self.wait.until(
                    EC.visibility_of_element_located(
                        (By.CSS_SELECTOR, AdminDashboardLocators.USERS_LINK) 
                    )
                )
                # Opsional: Tunggu page load lagi setelah elemen terlihat
                # self.wait_for_page_load() 
                print("[INFO] Login Admin Berhasil, Dashboard admin terlihat.")
                
            except TimeoutException:
                # Jika elemen admin tidak muncul, cek apakah ada pesan error login atau jika masih di halaman login.
                current_url = self.driver.current_url
                if "/login" in current_url:
                    # Asumsi BasePage memiliki is_element_visible() yang menggunakan timeout pendek (misal 3 detik)
                    if self.is_element_visible(self.locators.ERROR_MESSAGE, timeout=3):
                        raise Exception(f"Login Gagal: {self.get_text(self.locators.ERROR_MESSAGE)}")
                
                raise TimeoutException("Login Gagal: Halaman Admin Dashboard tidak termuat setelah otentikasi.")