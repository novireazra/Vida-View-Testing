from pages.base_page import BasePage
from config.locators import LoginPageLocators
from selenium.webdriver.common.by import By

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
        self.input_text(self.locators.EMAIL_INPUT, email)
    
    def input_password(self, password):
        """Input password"""
        self.input_text(self.locators.PASSWORD_INPUT, password)
    
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
        self.wait_for_page_load()