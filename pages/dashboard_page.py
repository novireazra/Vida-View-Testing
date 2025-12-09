from pages.base_page import BasePage
from config.locators import DashboardLocators, NavbarLocators
from selenium.webdriver.common.by import By
import time

class DashboardPage(BasePage):
    def __init__(self, driver):
        super().__init__(driver)
        self.locators = DashboardLocators()
        self.navbar_locators = NavbarLocators()
    
    def navigate_to_tenant_dashboard(self):
        """Navigate ke tenant dashboard"""
        from config.config import Config
        self.navigate_to(f"{Config.BASE_URL}/tenant/dashboard")
        self.wait_for_page_load()
    
    def navigate_to_owner_dashboard(self):
        """Navigate ke owner dashboard"""
        from config.config import Config
        self.navigate_to(f"{Config.BASE_URL}/owner/dashboard")
        self.wait_for_page_load()
    
    def navigate_to_admin_dashboard(self):
        """Navigate ke admin dashboard"""
        from config.config import Config
        self.navigate_to(f"{Config.BASE_URL}/admin/dashboard")
        self.wait_for_page_load()
    
    def is_welcome_message_displayed(self):
        """Check apakah welcome message ditampilkan"""
        return self.is_element_visible(self.locators.WELCOME_MESSAGE, timeout=5)
    
    def get_stats_cards_count(self):
        """Get jumlah stats cards"""
        return len(self.find_elements(self.locators.STATS_CARD))
    
    def click_quick_action(self, action_text):
        """Click quick action link by text"""
        actions = self.find_elements(self.locators.QUICK_ACTION, By.XPATH)
        for action in actions:
            if action_text.lower() in action.text.lower():
                action.click()
                self.wait_for_page_load()
                return
    
    def logout(self):
        """Logout dari dashboard"""
        self.click(self.navbar_locators.PROFILE_BUTTON)
        time.sleep(0.5)
        self.click(self.navbar_locators.LOGOUT_BUTTON, By.XPATH)
        time.sleep(1)
    
    def click_notifications(self):
        """Click notifications bell"""
        self.click(self.navbar_locators.NOTIFICATION_BUTTON)
        self.wait_for_page_load()
    
    def get_unread_notification_count(self):
        """Get unread notification count"""
        if self.is_element_visible(self.navbar_locators.NOTIFICATION_BADGE, timeout=2):
            return self.get_text(self.navbar_locators.NOTIFICATION_BADGE)
        return "0"