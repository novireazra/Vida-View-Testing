from pages.base_page import BasePage
from config.locators import ApartmentsPageLocators, ApartmentDetailLocators
from selenium.webdriver.common.by import By
import time

class ApartmentsPage(BasePage):
    def __init__(self, driver):
        super().__init__(driver)
        self.locators = ApartmentsPageLocators()
    
    def navigate_to_apartments(self):
        """Navigate ke halaman apartments"""
        from config.config import Config
        self.navigate_to(f"{Config.BASE_URL}/apartments")
        self.wait_for_page_load()
    
    def search_apartment(self, keyword):
        """Search apartment"""
        self.input_text(self.locators.SEARCH_INPUT, keyword)
        time.sleep(1)  # Wait for search results
    
    def filter_by_status(self, status):
        """Filter by status (available/occupied)"""
        self.select_dropdown_by_value(self.locators.FILTER_STATUS, status)
        time.sleep(1)
    
    def get_apartment_cards_count(self):
        """Get jumlah apartment cards"""
        return len(self.find_elements(self.locators.APARTMENT_CARD))
    
    def click_first_apartment(self):
        """Click apartment pertama"""
        cards = self.find_elements(self.locators.APARTMENT_CARD)
        if cards:
            cards[0].click()
            self.wait_for_page_load()
    
    def click_apartment_by_index(self, index):
        """Click apartment by index (0-based)"""
        cards = self.find_elements(self.locators.APARTMENT_CARD)
        if len(cards) > index:
            cards[index].click()
            self.wait_for_page_load()
    
    def get_first_apartment_title(self):
        """Get title apartment pertama"""
        titles = self.find_elements(self.locators.APARTMENT_TITLE)
        return titles[0].text if titles else ""
    
    def get_first_apartment_price(self):
        """Get price apartment pertama"""
        prices = self.find_elements(self.locators.APARTMENT_PRICE)
        return prices[0].text if prices else ""
    
    def click_favorite_button(self, index=0):
        """Click favorite button"""
        buttons = self.find_elements(self.locators.FAVORITE_BUTTON)
        if len(buttons) > index:
            buttons[index].click()
            time.sleep(1)
    
    def is_no_results_displayed(self):
        """Check apakah 'no results' ditampilkan"""
        return self.is_element_visible(self.locators.NO_RESULTS, By.XPATH, timeout=3)

class ApartmentDetailPage(BasePage):
    def __init__(self, driver):
        super().__init__(driver)
        self.locators = ApartmentDetailLocators()
    
    def get_unit_number(self):
        """Get unit number"""
        return self.get_text(self.locators.UNIT_NUMBER)
    
    def get_unit_type(self):
        """Get unit type"""
        return self.get_text(self.locators.UNIT_TYPE)
    
    def get_price(self):
        """Get price"""
        return self.get_text(self.locators.PRICE)
    
    def click_booking_button(self):
        """Click booking button"""
        self.scroll_to_element(self.locators.BOOKING_BUTTON, By.XPATH)
        self.click(self.locators.BOOKING_BUTTON, By.XPATH)
        self.wait_for_page_load()
    
    def click_contact_owner(self):
        """Click contact owner button"""
        self.click(self.locators.CONTACT_OWNER_BUTTON, By.XPATH)
        time.sleep(1)
    
    def click_favorite(self):
        """Click favorite button"""
        self.click(self.locators.FAVORITE_BUTTON, By.XPATH)
        time.sleep(1)
    
    def click_back(self):
        """Click back button"""
        self.click(self.locators.BACK_BUTTON, By.XPATH)
        self.wait_for_page_load()
    
    def get_bedrooms_count(self):
        """Get jumlah bedrooms"""
        return self.get_text(self.locators.BEDROOMS, By.XPATH)
    
    def get_bathrooms_count(self):
        """Get jumlah bathrooms"""
        return self.get_text(self.locators.BATHROOMS, By.XPATH)
    
    def is_booking_button_visible(self):
        """Check apakah booking button visible"""
        return self.is_element_visible(self.locators.BOOKING_BUTTON, By.XPATH, timeout=3)