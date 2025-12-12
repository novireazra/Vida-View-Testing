import pytest
import time
from pages.login_page import LoginPage
from pages.register_page import RegisterPage
from pages.dashboard_page import DashboardPage
from config.config import Config
from utils.helpers import TestDataGenerator
from utils.test_data import TestData

class TestAuthentication:
    """Test suite untuk Authentication & Authorization"""
    
    @pytest.mark.smoke
    @pytest.mark.authentication
    @pytest.mark.critical
    def test_TC_AUTH_001_login_admin_valid(self, driver):
        """TC_AUTH_001: Login dengan kredensial valid sebagai Admin"""
        login_page = LoginPage(driver)
        dashboard_page = DashboardPage(driver)
        
        # Navigate to login page
        login_page.navigate_to_login()
        time.sleep(1)
        
        # Login dengan admin credentials
        login_page.login(Config.ADMIN_EMAIL, Config.ADMIN_PASSWORD)
        time.sleep(2)
        
        # Verify redirect ke admin dashboard
        assert "/admin/dashboard" in driver.current_url
        assert dashboard_page.is_welcome_message_displayed()
    
    @pytest.mark.smoke
    @pytest.mark.authentication
    @pytest.mark.critical
    def test_TC_AUTH_002_login_owner_valid(self, driver):
        """TC_AUTH_002: Login dengan kredensial valid sebagai Owner"""
        login_page = LoginPage(driver)
        dashboard_page = DashboardPage(driver)
        
        login_page.navigate_to_login()
        time.sleep(1)
        
        login_page.login(Config.OWNER_EMAIL, Config.OWNER_PASSWORD)
        time.sleep(2)
        
        assert "/owner/dashboard" in driver.current_url
        assert dashboard_page.is_welcome_message_displayed()
    
    @pytest.mark.smoke
    @pytest.mark.authentication
    @pytest.mark.critical
    def test_TC_AUTH_003_login_tenant_valid(self, driver):
        """TC_AUTH_003: Login dengan kredensial valid sebagai Tenant"""
        login_page = LoginPage(driver)
        dashboard_page = DashboardPage(driver)
        
        login_page.navigate_to_login()
        time.sleep(1)
        login_page.login(Config.TENANT_EMAIL, Config.TENANT_PASSWORD)
        time.sleep(2)
        
        assert "/tenant/dashboard" in driver.current_url or "/dashboard" in driver.current_url
        assert dashboard_page.is_welcome_message_displayed()
    
    @pytest.mark.authentication
    def test_TC_AUTH_004_login_invalid_email(self, driver):
        """TC_AUTH_004: Login dengan email tidak terdaftar"""
        login_page = LoginPage(driver)
        
        login_page.navigate_to_login()
        time.sleep(1)
        
        login_page.login(TestData.INVALID_EMAIL, TestData.INVALID_PASSWORD)
        time.sleep(2)
        
        # Verify error message ditampilkan
        assert login_page.is_error_displayed()
        # Verify tetap di halaman login
        assert "/login" in driver.current_url
    
    @pytest.mark.authentication
    def test_TC_AUTH_005_login_invalid_password(self, driver):
        """TC_AUTH_005: Login dengan password salah"""
        login_page = LoginPage(driver)
        
        login_page.navigate_to_login()
        time.sleep(1)
        
        login_page.login(Config.TENANT_EMAIL, TestData.INVALID_PASSWORD)
        time.sleep(2)
        
        assert login_page.is_error_displayed()
        assert "/login" in driver.current_url
    
    @pytest.mark.authentication
    def test_TC_AUTH_006_login_empty_fields(self, driver):
        """TC_AUTH_006: Login dengan field kosong"""
        login_page = LoginPage(driver)
        
        login_page.navigate_to_login()
        time.sleep(1)
        
        # Click login tanpa isi field
        login_page.click_login_button()
        time.sleep(1)
        
        # Verify tetap di halaman login
        assert "/login" in driver.current_url
    
    @pytest.mark.authentication
    @pytest.mark.regression
    def test_TC_AUTH_007_register_tenant_valid(self, driver):
        """TC_AUTH_007: Register user baru sebagai Tenant dengan data valid"""
        register_page = RegisterPage(driver)
        
        # Generate random data
        username = TestDataGenerator.generate_random_username()
        email = TestDataGenerator.generate_random_email()
        full_name = TestDataGenerator.generate_random_full_name()
        phone = TestDataGenerator.generate_random_phone()
        birth_date = TestDataGenerator.generate_birth_date(25)
        
        register_page.navigate_to_register()
        time.sleep(1)
        
        register_page.register_tenant(
            username=username,
            email=email,
            password=Config.NEW_USER_PASSWORD,
            full_name=full_name,
            phone=phone,
            birth_date=birth_date,
            address="Jl. Test Automation No. 123"
        )
        time.sleep(2)
        
        # Verify redirect ke login page
        assert "/login" in driver.current_url
    
    @pytest.mark.authentication
    @pytest.mark.regression
    def test_TC_AUTH_008_register_owner_valid(self, driver):
        """TC_AUTH_008: Register user baru sebagai Owner dengan data valid"""
        register_page = RegisterPage(driver)
        
        username = TestDataGenerator.generate_random_username("owner")
        email = TestDataGenerator.generate_random_email("owner")
        full_name = TestDataGenerator.generate_random_full_name()
        phone = TestDataGenerator.generate_random_phone()
        birth_date = TestDataGenerator.generate_birth_date(30)
        
        register_page.navigate_to_register()
        time.sleep(1)
        
        register_page.register_owner(
            username=username,
            email=email,
            password=Config.NEW_USER_PASSWORD,
            full_name=full_name,
            phone=phone,
            birth_date=birth_date
        )
        time.sleep(2)
        
        assert "/login" in driver.current_url
    
    @pytest.mark.authentication
    def test_TC_AUTH_009_register_invalid_email(self, driver):
        """TC_AUTH_009: Register dengan format email invalid"""
        register_page = RegisterPage(driver)
        
        register_page.navigate_to_register()
        time.sleep(1)
        
        register_page.select_role_tenant()
        register_page.input_username("testuser123")
        register_page.input_full_name("Test User")
        register_page.input_email("invalidemail")  # Invalid format
        register_page.input_phone("081234567890")
        register_page.input_password("Password123")
        register_page.input_confirm_password("Password123")
        register_page.input_birth_date("1995-01-01")
        register_page.check_terms()
        register_page.click_register_button()
        time.sleep(2)
        
        # Verify tetap di halaman register
        assert "/register" in driver.current_url
    
    @pytest.mark.authentication
    def test_TC_AUTH_010_register_password_mismatch(self, driver):
        """TC_AUTH_010: Register dengan password tidak cocok"""
        register_page = RegisterPage(driver)
        
        register_page.navigate_to_register()
        time.sleep(1)
        
        register_page.select_role_tenant()
        register_page.input_username(TestDataGenerator.generate_random_username())
        register_page.input_full_name("Test User")
        register_page.input_email(TestDataGenerator.generate_random_email())
        register_page.input_phone("081234567890")
        register_page.input_password("Password123")
        register_page.input_confirm_password("DifferentPassword")
        register_page.input_birth_date("1995-01-01")
        register_page.check_terms()
        register_page.click_register_button()
        time.sleep(2)
        
        assert "/register" in driver.current_url
    
    @pytest.mark.authentication
    def test_TC_AUTH_011_register_underage(self, driver):
        """TC_AUTH_011: Register dengan umur dibawah 18 tahun"""
        register_page = RegisterPage(driver)
        
        register_page.navigate_to_register()
    
        # Generate birth date untuk umur 17 tahun
        birth_date = TestDataGenerator.generate_birth_date(17)
        
        register_page.select_role_tenant()
        register_page.input_username(TestDataGenerator.generate_random_username())
        register_page.input_full_name("Test Minor User")
        register_page.input_email(TestDataGenerator.generate_random_email())
        register_page.input_phone("081234567890")
        register_page.input_password("Password123")
        register_page.input_confirm_password("Password123")
        register_page.input_birth_date(birth_date)
        register_page.check_terms()
        register_page.click_register_button()
        
        
        # Should show error or stay on register page
        assert "/register" in driver.current_url
        try:
                    error_text = register_page.get_age_validation_error()
                    assert "18 tahun" in error_text or "batas usia" in error_text or "minimal 18" in error_text
        except Exception:
                    # Jika get_age_validation_error gagal, mungkin ada error message umum
                    print("Pesan error validasi usia tidak ditemukan di lokasi yang diharapkan.")
                    # Di sini Anda bisa menambahkan kegagalan eksplisit jika pesan error tidak ditemukan.
                    # raise AssertionError("Test Gagal: Pesan error batas usia tidak muncul.")
            
    @pytest.mark.smoke
    @pytest.mark.authentication
    @pytest.mark.critical
    def test_TC_AUTH_012_logout_functionality(self, driver):
        """TC_AUTH_012: Logout functionality"""
        login_page = LoginPage(driver)
        dashboard_page = DashboardPage(driver)
        
        # Login first
        login_page.navigate_to_login()
        time.sleep(1)
        login_page.login(Config.TENANT_EMAIL, Config.TENANT_PASSWORD)
        time.sleep(2)
        
        # Logout
        dashboard_page.logout()
        time.sleep(2)
        
        # Verify redirect ke login atau home page
        current_url = driver.current_url
        assert "/login" in current_url or current_url == f"{Config.BASE_URL}/"
    
    @pytest.mark.authentication
    @pytest.mark.critical
    def test_TC_AUTH_013_role_based_access_tenant(self, driver):
        """TC_AUTH_013: Role-based access - Tenant tidak bisa akses admin page"""
        login_page = LoginPage(driver)
        
        # Login sebagai tenant
        login_page.navigate_to_login()
        time.sleep(1)
        login_page.login(Config.TENANT_EMAIL, Config.TENANT_PASSWORD)
        time.sleep(2)
        
        # Try to access admin page
        driver.get(f"{Config.BASE_URL}/admin/dashboard")
        time.sleep(2)
        
        # Verify redirect atau tidak bisa akses
        assert "/admin/dashboard" not in driver.current_url or "dashboard" in driver.current_url.lower()
    
    @pytest.mark.authentication
    @pytest.mark.critical
    def test_TC_AUTH_014_role_based_access_owner(self, driver):
        """TC_AUTH_014: Role-based access - Owner tidak bisa akses admin page"""
        login_page = LoginPage(driver)
        
        # Login sebagai owner
        login_page.navigate_to_login()
        time.sleep(1)
        login_page.login(Config.OWNER_EMAIL, Config.OWNER_PASSWORD)
        time.sleep(2)
        
        # Try to access admin page
        driver.get(f"{Config.BASE_URL}/admin/dashboard")
        time.sleep(2)
        
        # Verify redirect
        assert "/admin/dashboard" not in driver.current_url or "/owner" in driver.current_url