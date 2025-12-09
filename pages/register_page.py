from pages.base_page import BasePage
from config.locators import RegisterPageLocators
from selenium.webdriver.common.by import By
import time

class RegisterPage(BasePage):
    def __init__(self, driver):
        super().__init__(driver)
        self.locators = RegisterPageLocators()
    
    def navigate_to_register(self):
        """Navigate ke halaman register"""
        from config.config import Config
        self.navigate_to(f"{Config.BASE_URL}/register")
        self.wait_for_page_load()
    
    def select_role_tenant(self):
        """Pilih role tenant"""
        self.click(self.locators.ROLE_TENANT_BUTTON, By.XPATH)
        time.sleep(0.5)
    
    def select_role_owner(self):
        """Pilih role owner"""
        self.click(self.locators.ROLE_OWNER_BUTTON, By.XPATH)
        time.sleep(0.5)
    
    def input_username(self, username):
        """Input username"""
        self.input_text(self.locators.USERNAME_INPUT, username)
    
    def input_email(self, email):
        """Input email"""
        self.input_text(self.locators.EMAIL_INPUT, email)
    
    def input_password(self, password):
        """Input password"""
        self.input_text(self.locators.PASSWORD_INPUT, password)
    
    def input_confirm_password(self, password):
        """Input confirm password"""
        self.input_text(self.locators.CONFIRM_PASSWORD_INPUT, password)
    
    def input_full_name(self, full_name):
        """Input full name"""
        self.input_text(self.locators.FULL_NAME_INPUT, full_name)
    
    def input_phone(self, phone):
        """Input phone"""
        self.input_text(self.locators.PHONE_INPUT, phone)
    
    def input_birth_date(self, birth_date):
        """Input birth date (format: YYYY-MM-DD)"""
        self.input_text(self.locators.BIRTH_DATE_INPUT, birth_date)
    
    def input_address(self, address):
        """Input address"""
        self.input_text(self.locators.ADDRESS_INPUT, address)
    
    def check_terms(self):
        """Check terms checkbox"""
        self.click(self.locators.TERMS_CHECKBOX)
    
    def click_register_button(self):
        """Click register button"""
        self.click(self.locators.REGISTER_BUTTON)
    
    def register_tenant(self, username, email, password, full_name, phone, birth_date, address=""):
        """Complete tenant registration"""
        self.select_role_tenant()
        self.input_username(username)
        self.input_full_name(full_name)
        self.input_email(email)
        self.input_phone(phone)
        self.input_password(password)
        self.input_confirm_password(password)
        self.input_birth_date(birth_date)
        if address:
            self.input_address(address)
        self.check_terms()
        self.click_register_button()
        self.wait_for_page_load()
    
    def register_owner(self, username, email, password, full_name, phone, birth_date, address=""):
        """Complete owner registration"""
        self.select_role_owner()
        self.input_username(username)
        self.input_full_name(full_name)
        self.input_email(email)
        self.input_phone(phone)
        self.input_password(password)
        self.input_confirm_password(password)
        self.input_birth_date(birth_date)
        if address:
            self.input_address(address)
        self.check_terms()
        self.click_register_button()
        self.wait_for_page_load()