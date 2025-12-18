from pages.base_page import BasePage
from config.locators import LoginPageLocators, AdminDashboardLocators
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from config.config import Config


class LoginPage(BasePage):
    def __init__(self, driver):
        super().__init__(driver)
        self.locators = LoginPageLocators

    # =============================
    # NAVIGATION
    # =============================
    def navigate_to_login(self):
        """Navigasi ke halaman login"""
        self.navigate_to(f"{Config.BASE_URL}/login")
        self.wait_for_page_load()

    # =============================
    # PAGE STATE CHECK
    # =============================
    def is_login_form_visible(self):
        """Cek apakah form login terlihat"""
        return self.is_element_visible(self.locators.EMAIL_INPUT, timeout=3)

    def is_on_login_page(self):
        """Cek URL mengandung /login"""
        return "/login" in self.get_current_url()

    # =============================
    # INPUT ACTIONS
    # =============================
    def input_email(self, email):
        self.input_text(self.locators.EMAIL_INPUT, email)

    def input_password(self, password):
        self.input_text(self.locators.PASSWORD_INPUT, password)

    def click_login_button(self):
        self.click(self.locators.LOGIN_BUTTON)

    def check_remember_me(self):
        self.click(self.locators.REMEMBER_CHECKBOX)

    def click_register_link(self):
        self.click(self.locators.REGISTER_LINK)

    # =============================
    # ERROR HANDLING
    # =============================
    def is_error_displayed(self):
        return self.is_element_visible(self.locators.ERROR_MESSAGE, timeout=3)

    def get_error_message(self):
        return self.get_text(self.locators.ERROR_MESSAGE)

    # =============================
    # LOGIN FLOW
    # =============================
    def login(self, email, password, remember=False):
        """Alur login lengkap"""
        self.input_email(email)
        self.input_password(password)
        if remember:
            self.check_remember_me()
        self.click_login_button()

    # =============================
    # WAITERS
    # =============================
    def wait_for_login_form_load(self):
        """
        Menunggu form login.
        HANYA dipakai di test login,
        BUKAN di fixture global.
        """
        try:
            self.wait_for_page_load()
            self.find_element(self.locators.EMAIL_INPUT, timeout=10)
            print("[INFO] Halaman Login siap.")
        except Exception:
            self.refresh_page()
            try:
                self.find_element(self.locators.EMAIL_INPUT, timeout=10)
            except Exception:
                raise Exception(
                    f"Gagal memuat form login. URL saat ini: {self.get_current_url()}"
                )

    def wait_for_successful_admin_login(self):
        """Verifikasi login admin berhasil"""
        try:
            self.wait.until(
                EC.visibility_of_element_located(
                    AdminDashboardLocators.USERS_LINK
                )
            )
            print("[INFO] Login Admin berhasil.")
        except TimeoutException:
            if self.is_error_displayed():
                raise Exception(
                    f"Login gagal. Pesan error: {self.get_error_message()}"
                )
            raise TimeoutException(
                f"Dashboard Admin tidak muncul di {self.get_current_url()}"
            )
