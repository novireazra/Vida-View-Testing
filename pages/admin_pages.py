from pages.base_page import BasePage
from config.locators import (
    AdminDashboardLocators, 
    UserManagementLocators, 
    PromotionLocators
)
from selenium.webdriver.common.by import By
import time

class AdminDashboardPage(BasePage):
    def __init__(self, driver):
        super().__init__(driver)
        self.locators = AdminDashboardLocators()
    
    def navigate_to_users(self):
        """Navigate ke user management"""
        self.click(self.locators.USERS_LINK)
        self.wait_for_page_load()
    
    def navigate_to_bookings(self):
        """Navigate ke bookings management"""
        self.click(self.locators.BOOKINGS_LINK)
        self.wait_for_page_load()
    
    def navigate_to_payments(self):
        """Navigate ke payments"""
        self.click(self.locators.PAYMENTS_LINK)
        self.wait_for_page_load()
    
    def navigate_to_promotions(self):
        """Navigate ke promotions"""
        self.click(self.locators.PROMOTIONS_LINK)
        self.wait_for_page_load()
    
    def navigate_to_reports(self):
        """Navigate ke reports"""
        self.click(self.locators.REPORTS_LINK)
        self.wait_for_page_load()

class UserManagementPage(BasePage):
    def __init__(self, driver):
        super().__init__(driver)
        self.locators = UserManagementLocators()
    
    def search_user(self, keyword):
        """Search user"""
        self.input_text(self.locators.SEARCH_INPUT, keyword)
        time.sleep(1)
    
    def filter_by_role(self, role):
        """Filter by role (tenant/owner/admin)"""
        self.select_dropdown_by_value(self.locators.ROLE_FILTER, role)
        time.sleep(1)
    
    def filter_by_status(self, status):
        """Filter by status (active/inactive)"""
        self.select_dropdown_by_value(self.locators.STATUS_FILTER, status)
        time.sleep(1)
    
    def get_user_rows_count(self):
        """Get jumlah user rows"""
        return len(self.find_elements(self.locators.USER_ROW))
    
    def click_edit_first_user(self):
        """Click edit button user pertama"""
        buttons = self.find_elements(self.locators.EDIT_BUTTON)
        if buttons:
            buttons[0].click()
            time.sleep(1)
    
    def click_view_documents(self, index=0):
        """Click view documents button"""
        buttons = self.find_elements(self.locators.VIEW_DOCS_BUTTON)
        if len(buttons) > index:
            buttons[index].click()
            time.sleep(1)
    
    def click_verify_documents(self, index=0):
        """Click verify documents button"""
        buttons = self.find_elements(self.locators.VERIFY_BUTTON)
        if len(buttons) > index:
            buttons[index].click()
            time.sleep(1)
    
    def confirm_verify(self):
        """Confirm verify di modal"""
        self.click(self.locators.SAVE_BUTTON, By.XPATH)
        time.sleep(2)
    
    def click_delete_user(self, index=0):
        """Click delete user button"""
        buttons = self.find_elements(self.locators.DELETE_BUTTON)
        if len(buttons) > index:
            buttons[index].click()
            time.sleep(1)
    
    def confirm_delete(self):
        """Confirm delete di modal"""
        self.click(self.locators.CONFIRM_DELETE_BUTTON, By.XPATH)
        time.sleep(2)

class PromotionManagementPage(BasePage):
    def __init__(self, driver):
        super().__init__(driver)
        self.locators = PromotionLocators()
    
    def click_add_promotion(self):
        """Click add promotion button"""
        self.click(self.locators.ADD_PROMO_BUTTON, By.XPATH)
        time.sleep(1)
    
    def input_promo_code(self, code):
        """Input promo code"""
        self.input_text(self.locators.PROMO_CODE_INPUT, code)
    
    def input_promo_title(self, title):
        """Input promo title"""
        self.input_text(self.locators.PROMO_TITLE_INPUT, title)
    
    def select_promo_type(self, promo_type):
        """Select promo type (percent/fixed_amount)"""
        self.select_dropdown_by_value(self.locators.PROMO_TYPE_SELECT, promo_type)
    
    def input_promo_value(self, value):
        """Input promo value"""
        self.input_text(self.locators.PROMO_VALUE_INPUT, str(value))
    
    def input_start_date(self, date):
        """Input start date"""
        self.input_text(self.locators.START_DATE_INPUT, date)
    
    def input_end_date(self, date):
        """Input end date"""
        self.input_text(self.locators.END_DATE_INPUT, date)
    
    def check_active(self):
        """Check active checkbox"""
        checkboxes = self.find_elements(self.locators.ACTIVE_CHECKBOX)
        if checkboxes and not checkboxes[0].is_selected():
            checkboxes[0].click()
    
    def click_submit(self):
        """Click submit button"""
        self.click(self.locators.SUBMIT_BUTTON, By.XPATH)
        time.sleep(2)
    
    def create_promotion(self, code, title, promo_type, value, start_date, end_date):
        """Create new promotion"""
        self.click_add_promotion()
        self.input_promo_code(code)
        self.input_promo_title(title)
        self.select_promo_type(promo_type)
        self.input_promo_value(value)
        self.input_start_date(start_date)
        self.input_end_date(end_date)
        self.check_active()
        self.click_submit()
    
    def get_promotion_cards_count(self):
        """Get jumlah promotion cards"""
        return len(self.find_elements(self.locators.PROMO_CARD))
    
    def click_edit_first_promotion(self):
        """Click edit promotion pertama"""
        buttons = self.find_elements(self.locators.EDIT_BUTTON, By.XPATH)
        if buttons:
            buttons[0].click()
            time.sleep(1)
    
    def click_delete_first_promotion(self):
        """Click delete promotion pertama"""
        buttons = self.find_elements(self.locators.DELETE_BUTTON, By.XPATH)
        if buttons:
            buttons[0].click()
            time.sleep(1)