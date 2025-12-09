from pages.base_page import BasePage
from config.locators import PaymentPageLocators
from selenium.webdriver.common.by import By
import time

class PaymentPage(BasePage):
    def __init__(self, driver):
        super().__init__(driver)
        self.locators = PaymentPageLocators()
    
    def select_bank_transfer(self):
        """Select bank transfer payment method"""
        self.click(self.locators.BANK_TRANSFER_OPTION, By.XPATH)
        time.sleep(0.5)
    
    def select_credit_card(self):
        """Select credit card payment method"""
        self.click(self.locators.CREDIT_CARD_OPTION, By.XPATH)
        time.sleep(0.5)
    
    def select_ewallet(self):
        """Select e-wallet payment method"""
        self.click(self.locators.EWALLET_OPTION, By.XPATH)
        time.sleep(0.5)
    
    def click_next(self):
        """Click next button"""
        self.click(self.locators.NEXT_BUTTON, By.XPATH)
        time.sleep(1)
    
    def click_previous(self):
        """Click previous button"""
        self.click(self.locators.PREVIOUS_BUTTON, By.XPATH)
        time.sleep(1)
    
    def input_transaction_id(self, transaction_id):
        """Input transaction ID"""
        self.input_text(self.locators.TRANSACTION_ID_INPUT, transaction_id)
    
    def upload_receipt(self, filepath):
        """Upload receipt file"""
        self.upload_file(self.locators.RECEIPT_UPLOAD, filepath)
        time.sleep(1)
    
    def input_notes(self, notes):
        """Input notes"""
        self.input_text(self.locators.NOTES_INPUT, notes)
    
    def click_confirm_payment(self):
        """Click confirm payment button"""
        self.scroll_to_element(self.locators.CONFIRM_BUTTON, By.XPATH)
        self.click(self.locators.CONFIRM_BUTTON, By.XPATH)
        time.sleep(2)
    
    def complete_payment_bank_transfer(self, transaction_id, receipt_path="", notes=""):
        """Complete payment dengan bank transfer"""
        self.select_bank_transfer()
        self.click_next()
        self.click_next()  # Skip bank info page
        self.input_transaction_id(transaction_id)
        if receipt_path:
            self.upload_receipt(receipt_path)
        if notes:
            self.input_notes(notes)
        self.click_confirm_payment()
        