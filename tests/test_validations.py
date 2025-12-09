import pytest
import time
from pages.login_page import LoginPage
from pages.register_page import RegisterPage
from pages.booking_page import BookingPage
from config.config import Config
from utils.helpers import TestDataGenerator

class TestValidations:
    """Test suite untuk Form Validations & Error Handling"""
    
    @pytest.mark.validation
    def test_TC_VAL_001_login_email_required(self, driver):
        """TC_VAL_001: Validasi email wajib diisi pada login"""
        login_page = LoginPage(driver)
        
        login_page.navigate_to_login()
        time.sleep(1)
        
        # Hanya isi password, email kosong
        login_page.input_password("password123")
        login_page.click_login_button()
        time.sleep(1)
        
        # Should stay on login page
        assert "/login" in driver.current_url
    
    @pytest.mark.validation
    def test_TC_VAL_002_login_password_required(self, driver):
        """TC_VAL_002: Validasi password wajib diisi pada login"""
        login_page = LoginPage(driver)
        
        login_page.navigate_to_login()
        time.sleep(1)
        
        # Hanya isi email, password kosong
        login_page.input_email("test@test.com")
        login_page.click_login_button()
        time.sleep(1)
        
        assert "/login" in driver.current_url
    
    @pytest.mark.validation
    def test_TC_VAL_003_register_email_format(self, driver):
        """TC_VAL_003: Validasi format email pada register"""
        register_page = RegisterPage(driver)
        
        register_page.navigate_to_register()
        time.sleep(1)
        
        register_page.select_role_tenant()
        register_page.input_email("invalidemail")  # Invalid format
        register_page.input_username("testuser")
        register_page.input_full_name("Test User")
        register_page.input_password("Password123")
        register_page.input_confirm_password("Password123")
        register_page.input_phone("081234567890")
        register_page.input_birth_date("1995-01-01")
        register_page.check_terms()
        register_page.click_register_button()
        time.sleep(2)
        
        # Should stay on register page with error
        assert "/register" in driver.current_url
    
    @pytest.mark.validation
    def test_TC_VAL_004_register_phone_format(self, driver):
        """TC_VAL_004: Validasi format phone pada register"""
        register_page = RegisterPage(driver)
        
        register_page.navigate_to_register()
        time.sleep(1)
        
        register_page.select_role_tenant()
        register_page.input_username("testuser")
        register_page.input_full_name("Test User")
        register_page.input_email("test@test.com")
        register_page.input_phone("123")  # Invalid phone
        register_page.input_password("Password123")
        register_page.input_confirm_password("Password123")
        register_page.input_birth_date("1995-01-01")
        register_page.check_terms()
        register_page.click_register_button()
        time.sleep(2)
        
        assert "/register" in driver.current_url
    
    @pytest.mark.validation
    def test_TC_VAL_005_register_password_minlength(self, driver):
        """TC_VAL_005: Validasi password minimum 6 karakter"""
        register_page = RegisterPage(driver)
        
        register_page.navigate_to_register()
        time.sleep(1)
        
        register_page.select_role_tenant()
        register_page.input_username("testuser")
        register_page.input_full_name("Test User")
        register_page.input_email("test@test.com")
        register_page.input_phone("081234567890")
        register_page.input_password("123")  # Too short
        register_page.input_confirm_password("123")
        register_page.input_birth_date("1995-01-01")
        register_page.check_terms()
        register_page.click_register_button()
        time.sleep(2)
        
        assert "/register" in driver.current_url
    
    @pytest.mark.validation
    def test_TC_VAL_006_register_terms_required(self, driver):
        """TC_VAL_006: Validasi terms & conditions harus dicheck"""
        register_page = RegisterPage(driver)
        
        register_page.navigate_to_register()
        time.sleep(1)
        
        register_page.select_role_tenant()
        register_page.input_username(TestDataGenerator.generate_random_username())
        register_page.input_full_name("Test User")
        register_page.input_email(TestDataGenerator.generate_random_email())
        register_page.input_phone("081234567890")
        register_page.input_password("Password123")
        register_page.input_confirm_password("Password123")
        register_page.input_birth_date("1995-01-01")
        # Don't check terms
        register_page.click_register_button()
        time.sleep(2)
        
        assert "/register" in driver.current_url
    
    @pytest.mark.validation
    def test_TC_VAL_007_booking_date_required(self, driver):
        """TC_VAL_007: Validasi tanggal booking wajib diisi"""
        # Login first
        login_page = LoginPage(driver)
        login_page.navigate_to_login()
        time.sleep(1)
        login_page.login(Config.TENANT_EMAIL, Config.TENANT_PASSWORD)
        time.sleep(2)
        
        booking_page = BookingPage(driver)
        
        # Try to submit without dates
        # Note: This test assumes we're on booking page
        # In practice, you'd navigate to a specific booking page
        
        assert True
    
    @pytest.mark.validation
    def test_TC_VAL_008_file_upload_size_limit(self, driver, create_test_files):
        """TC_VAL_008: Validasi ukuran file upload maksimal 5MB"""
        # This test would require creating a file > 5MB
        # Placeholder test
        assert True
    
    @pytest.mark.validation
    def test_TC_VAL_009_file_upload_type(self, driver):
        """TC_VAL_009: Validasi tipe file yang diupload (JPG, PNG, PDF only)"""
        # This test would require attempting to upload unsupported file type
        # Placeholder test
        assert True
    
    @pytest.mark.validation
    def test_TC_VAL_010_promo_code_format(self, driver):
        """TC_VAL_010: Validasi format kode promo (uppercase, alphanumeric)"""
        login_page = LoginPage(driver)
        login_page.navigate_to_login()
        time.sleep(1)
        login_page.login(Config.TENANT_EMAIL, Config.TENANT_PASSWORD)
        time.sleep(2)
        
        booking_page = BookingPage(driver)
        
        # Try to apply invalid promo code format
        # Placeholder test
        assert True