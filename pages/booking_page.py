from pages.base_page import BasePage
from config.locators import BookingPageLocators
from selenium.webdriver.common.by import By
import time

class BookingPage(BasePage):
    def __init__(self, driver):
        super().__init__(driver)
        self.locators = BookingPageLocators()
    
    def input_start_date(self, date):
        """Input start date (format: YYYY-MM-DD)"""
        self.input_text(self.locators.START_DATE_INPUT, date)
        time.sleep(0.5)
    
    def input_end_date(self, date):
        """Input end date (format: YYYY-MM-DD)"""
        self.input_text(self.locators.END_DATE_INPUT, date)
        time.sleep(0.5)
    
    def input_notes(self, notes):
        """Input notes"""
        self.input_text(self.locators.NOTES_TEXTAREA, notes)
    
    def input_promo_code(self, code):
        """Input promo code"""
        self.input_text(self.locators.PROMO_CODE_INPUT, code)
    
    def click_apply_promo(self):
        """Click apply promo button"""
        self.click(self.locators.APPLY_PROMO_BUTTON, By.XPATH)
        time.sleep(2)  # Wait for promo validation
    
    def click_remove_promo(self):
        """Click remove promo button"""
        self.click(self.locators.REMOVE_PROMO_BUTTON, By.XPATH)
        time.sleep(1)
    
    def get_total_amount(self):
        """Get total amount"""
        return self.get_text(self.locators.SUMMARY_TOTAL)
    
    def is_promo_applied(self):
        """Check apakah promo sudah applied"""
        return self.is_element_visible(self.locators.APPLIED_PROMO_CODE, timeout=3)
    
    def get_applied_promo_code(self):
        """Get applied promo code"""
        if self.is_promo_applied():
            return self.get_text(self.locators.APPLIED_PROMO_CODE)
        return ""
    
    def click_submit(self):
        """Click submit booking button"""
        self.scroll_to_element(self.locators.SUBMIT_BUTTON)
        self.click(self.locators.SUBMIT_BUTTON)
        time.sleep(2)
    
    def click_back(self):
        """Click back button"""
        self.click(self.locators.BACK_BUTTON, By.XPATH)
    
    def create_booking(self, start_date, end_date, notes="", promo_code=""):
        """Complete booking flow"""
        self.input_start_date(start_date)
        self.input_end_date(end_date)
        if notes:
            self.input_notes(notes)
        if promo_code:
            self.input_promo_code(promo_code)
            self.click_apply_promo()
        time.sleep(1)  # Wait for calculation
        self.click_submit()