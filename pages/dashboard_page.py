from pages.base_page import BasePage
from config.locators import DashboardLocators, NavbarLocators
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import (
    TimeoutException,
    ElementClickInterceptedException
)

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
        """
        Logout dari dashboard (FIXED)
        - Menunggu overlay React hilang
        - Anti ElementClickInterceptedException
        - JS fallback jika perlu
        """

        wait = WebDriverWait(self.driver, 15)

        # 1️⃣ Tunggu overlay/loading React menghilang
        try:
            wait.until(
                EC.invisibility_of_element_located((
                    By.CSS_SELECTOR,
                    "div.fixed.inset-0.bg-white.bg-opacity-75"
                ))
            )
        except TimeoutException:
            print("[WARNING] Overlay tidak hilang, lanjutkan proses logout")

        # 2️⃣ Klik tombol profile
        profile_btn = wait.until(
            EC.element_to_be_clickable(self.navbar_locators.PROFILE_BUTTON)
        )

        try:
            profile_btn.click()
        except ElementClickInterceptedException:
            self.driver.execute_script(
                "arguments[0].click();", profile_btn
            )

        # 3️⃣ Klik tombol logout
        logout_btn = wait.until(
            EC.element_to_be_clickable(self.navbar_locators.LOGOUT_BUTTON)
        )
        logout_btn.click()
    
    def click_notifications(self):
        """Click notifications bell"""
        self.click(self.navbar_locators.NOTIFICATION_BUTTON)
        self.wait_for_page_load()
    
    def get_unread_notification_count(self):
        """Get unread notification count"""
        if self.is_element_visible(self.navbar_locators.NOTIFICATION_BADGE, timeout=2):
            return self.get_text(self.navbar_locators.NOTIFICATION_BADGE)
        return "0"
