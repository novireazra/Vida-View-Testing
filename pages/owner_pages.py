from pages.base_page import BasePage
from config.locators import OwnerUnitsLocators, AddUnitModalLocators
from selenium.webdriver.common.by import By
import time

class OwnerUnitsPage(BasePage):
    def __init__(self, driver):
        super().__init__(driver)
        self.locators = OwnerUnitsLocators()
    
    def navigate_to_my_units(self):
        """Navigate ke my units page"""
        from config.config import Config
        self.navigate_to(f"{Config.BASE_URL}/owner/units")
        self.wait_for_page_load()
    
    def click_add_unit(self):
        try:
            self.click(self.locators.ADD_UNIT_BUTTON, By.XPATH)
        except:
            print("Normal click gagal, mencoba force_click...")
            self.force_click(self.locators.ADD_UNIT_BUTTON, By.XPATH)
        time.sleep(1)

    
    def filter_all_units(self):
        """Filter semua units"""
        self.click(self.locators.FILTER_ALL, By.XPATH)
        time.sleep(1)
    
    def filter_available_units(self):
        """Filter available units"""
        self.click(self.locators.FILTER_AVAILABLE, By.XPATH)
        time.sleep(1)
    
    def filter_occupied_units(self):
        """Filter occupied units"""
        self.click(self.locators.FILTER_OCCUPIED, By.XPATH)
        time.sleep(1)
    
    def get_units_count(self):
        """Get jumlah units"""
        return len(self.find_elements(self.locators.UNIT_CARD))
    
    def click_view_first_unit(self):
        """Click view detail first unit"""
        buttons = self.find_elements(self.locators.VIEW_BUTTON)
        if buttons:
            buttons[0].click()
            self.wait_for_page_load()
    
    def click_edit_first_unit(self):
        """Click edit first unit"""
        buttons = self.find_elements(self.locators.EDIT_BUTTON)
        if buttons:
            buttons[0].click()
            time.sleep(1)
    
    def click_delete_first_unit(self):
        """Click delete first unit"""
        buttons = self.find_elements(self.locators.DELETE_BUTTON)
        if buttons:
            buttons[0].click()
            time.sleep(1)
    
    def click_archive_first_unit(self):
        """Click archive first unit"""
        buttons = self.find_elements(self.locators.ARCHIVE_BUTTON)
        if buttons:
            buttons[0].click()
            time.sleep(1)

class AddUnitModal(BasePage):
    def __init__(self, driver):
        super().__init__(driver)
        self.locators = AddUnitModalLocators()
    
    def input_unit_number(self, unit_number):
        """Input unit number"""
        self.input_text(self.locators.UNIT_NUMBER_INPUT, unit_number)
    
    def select_unit_type(self, unit_type):
        """Select unit type"""
        self.select_dropdown_by_value(self.locators.UNIT_TYPE_SELECT, unit_type)
    
    def input_bedrooms(self, bedrooms):
        """Input bedrooms"""
        self.input_text(self.locators.BEDROOMS_INPUT, str(bedrooms))
    
    def input_bathrooms(self, bathrooms):
        """Input bathrooms"""
        self.input_text(self.locators.BATHROOMS_INPUT, str(bathrooms))
    
    def input_size(self, size):
        """Input size"""
        self.input_text(self.locators.SIZE_INPUT, str(size))
    
    def input_floor(self, floor):
        """Input floor"""
        self.input_text(self.locators.FLOOR_INPUT, str(floor))
    
    def input_price(self, price):
        """Input price"""
        self.input_text(self.locators.PRICE_INPUT, str(price))
    
    def input_deposit(self, deposit):
        """Input deposit"""
        self.input_text(self.locators.DEPOSIT_INPUT, str(deposit))
    
    def input_description(self, description):
        """Input description"""
        self.input_text(self.locators.DESCRIPTION_TEXTAREA, description)
    
    def check_furnished(self):
        """Check furnished checkbox"""
        checkboxes = self.find_elements(self.locators.FURNISHED_CHECKBOX)
        if checkboxes and not checkboxes[0].is_selected():
            checkboxes[0].click()
    
    def upload_photos(self, photo_paths):
        """Upload multiple photos"""
        for path in photo_paths:
            self.upload_file(self.locators.PHOTO_UPLOAD, path)
            time.sleep(0.5)
    
    def click_submit(self):
        """Click submit button"""
        self.scroll_to_element(self.locators.SUBMIT_BUTTON, By.XPATH)
        self.click(self.locators.SUBMIT_BUTTON, By.XPATH)
        time.sleep(2)
    
    def click_cancel(self):
        """Click cancel button"""
        self.click(self.locators.CANCEL_BUTTON, By.XPATH)
        time.sleep(1)
    
    def add_unit(self, unit_number, unit_type, bedrooms, bathrooms, size, floor, price, deposit, description="", furnished=True):
        """Add complete unit"""
        self.input_unit_number(unit_number)
        self.select_unit_type(unit_type)
        self.input_bedrooms(bedrooms)
        self.input_bathrooms(bathrooms)
        self.input_size(size)
        self.input_floor(floor)
        self.input_price(price)
        self.input_deposit(deposit)
        if description:
            self.input_description(description)
        if furnished:
            self.check_furnished()
        self.click_submit()