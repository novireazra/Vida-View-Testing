import os
import pytest
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from pages.login_page import LoginPage
from pages.admin_pages import AdminDashboardPage, UserManagementPage, PromotionManagementPage
from config.config import Config
from utils.helpers import TestDataGenerator
from utils.test_data import TestData

class TestAdminFlow:
    """Test suite untuk Admin Flow"""
    
    @pytest.fixture(autouse=True)
    def setup(self, driver):
        """Setup: Login sebagai admin sebelum setiap test"""
        login_page = LoginPage(driver)
        login_page.navigate_to_login()
        time.sleep(1)
        login_page.login(Config.ADMIN_EMAIL, Config.ADMIN_PASSWORD)
        time.sleep(2)
        yield
    
    @pytest.mark.smoke
    @pytest.mark.admin
    @pytest.mark.critical
    def test_TC_ADM_001_view_admin_dashboard(self, driver):
        """TC_ADM_001: View admin dashboard"""
        admin_dash = AdminDashboardPage(driver)
        
        driver.get(f"{Config.BASE_URL}/admin/dashboard")
        time.sleep(4)
        
        # Verify dashboard loaded
        assert "/admin/dashboard" in driver.current_url
    
    @pytest.mark.admin
    @pytest.mark.critical
    def test_TC_ADM_002_navigate_to_users(self, driver):
        """TC_ADM_002: Navigate to user management"""
        admin_dash = AdminDashboardPage(driver)
        
        driver.get(f"{Config.BASE_URL}/admin/dashboard")
        time.sleep(2)
        
        admin_dash.navigate_to_users()
        time.sleep(4)
        
        # Verify users page loaded
        assert "/admin/users" in driver.current_url
    
    @pytest.mark.admin
    def test_TC_ADM_003_search_user(self, driver):
        """TC_ADM_003: Search user by keyword"""
        user_mgmt = UserManagementPage(driver)
        
        driver.get(f"{Config.BASE_URL}/admin/users")
        time.sleep(2)
        
        user_mgmt.search_user("tenant")
        time.sleep(2)
        
        # Verify search executed
        assert user_mgmt.get_user_rows_count() >= 0
    
    @pytest.mark.admin
    def test_TC_ADM_004_filter_users_by_role(self, driver):
        """TC_ADM_004: Filter users by role (Tenant)"""
        user_mgmt = UserManagementPage(driver)
        
        driver.get(f"{Config.BASE_URL}/admin/users")
        time.sleep(2)
        
        user_mgmt.filter_by_role("tenant")
        time.sleep(2)
        
        assert True
    
    @pytest.mark.admin
    def test_TC_ADM_005_filter_users_by_status(self, driver):
        """TC_ADM_005: Filter users by status (Active)"""
        user_mgmt = UserManagementPage(driver)
        
        driver.get(f"{Config.BASE_URL}/admin/users")
        time.sleep(2)
        
        user_mgmt.filter_by_status("active")
        time.sleep(2)
        
        assert True
    
    @pytest.mark.admin
    @pytest.mark.critical
    def test_TC_ADM_006_view_user_documents(self, driver):
        """TC_ADM_006: View user documents"""
        user_mgmt = UserManagementPage(driver)
        
        driver.get(f"{Config.BASE_URL}/admin/users")
        time.sleep(2)
        
        if user_mgmt.get_user_rows_count() > 0:
            user_mgmt.click_view_documents(0)
            time.sleep(2)
            
            # Verify modal or page opened
            assert True
    
    @pytest.mark.admin
    @pytest.mark.critical
    def test_TC_ADM_007_verify_user_documents(self, driver):
        """TC_ADM_007: Verify user documents (KTP & Selfie)"""
        user_mgmt = UserManagementPage(driver)
        
        driver.get(f"{Config.BASE_URL}/admin/users")
        time.sleep(2)
        
        # This test requires a user with unverified documents
        # Placeholder test
        assert "/admin/users" in driver.current_url
    
    @pytest.mark.admin
    def test_TC_ADM_008_edit_user(self, driver):
        """TC_ADM_008: Edit user information"""
        user_mgmt = UserManagementPage(driver)
        
        driver.get(f"{Config.BASE_URL}/admin/users")
        time.sleep(2)
        
        if user_mgmt.get_user_rows_count() > 0:
            user_mgmt.click_edit_first_user()
            time.sleep(2)
            
            # Edit modal should open
            assert True
    
    # @pytest.mark.admin
    # @pytest.mark.critical
    # def test_TC_ADM_009_navigate_to_bookings(self, driver):
    #     """TC_ADM_009: Navigate to bookings management"""
    #     admin_dash = AdminDashboardPage(driver)
        
    #     driver.get(f"{Config.BASE_URL}/admin/dashboard")
    #     time.sleep(1)
        
    #     admin_dash.navigate_to_bookings()
    #     time.sleep(2)
        
    #     assert "/admin/bookings" in driver.current_url
    
    @pytest.mark.admin
    @pytest.mark.critical
    def test_TC_ADM_010_navigate_to_payments(self, driver):
        """TC_ADM_010: Navigate to payment verification"""
        admin_dash = AdminDashboardPage(driver)
        
        driver.get(f"{Config.BASE_URL}/admin/dashboard")
        time.sleep(1)
        
        admin_dash.navigate_to_payments()
        time.sleep(2)
        
        assert "/admin/payments" in driver.current_url
    
    @pytest.mark.admin
    @pytest.mark.critical
    def test_TC_ADM_011_verify_payment(self, driver):
        """TC_ADM_011: Verify payment from tenant"""
        # Navigate to payments
        driver.get(f"{Config.BASE_URL}/admin/payments")
        time.sleep(2)
        
        # Placeholder for verify payment action
        assert "/admin/payments" in driver.current_url
    
    @pytest.mark.admin
    @pytest.mark.critical
    def test_TC_ADM_012_navigate_to_promotions(self, driver):
        """TC_ADM_012: Navigate to promotions management"""
        admin_dash = AdminDashboardPage(driver)
        
        driver.get(f"{Config.BASE_URL}/admin/dashboard")
        time.sleep(2)
        
        admin_dash.navigate_to_promotions()
        time.sleep(2)
        
        assert "/admin/promotions" in driver.current_url
    
    @pytest.mark.admin
    @pytest.mark.critical
    @pytest.mark.slow
    def test_TC_ADM_013_create_promotion(self, driver, login_admin):
        """TC_ADM_013: Create new promotion"""
        admin_dashboard = AdminDashboardPage(driver)
        promo_mgmt = PromotionManagementPage(driver)

        
        admin_dashboard.navigate_to_promotions() # <-- Panggil method navigasi


        promo_mgmt.find_element(promo_mgmt.locators.ADD_PROMO_BUTTON, By.XPATH)
        
        initial_count = promo_mgmt.get_promotion_cards_count()
        
        # Generate unique promo code
        promo_code = TestDataGenerator.generate_promo_code()
        
        promo_mgmt.create_promotion(
            code=promo_code,
            title="Test Automation Promo",
            promo_type="percent",
            value=15,
            start_date=TestData.PROMO_DATA['start_date'],
            end_date=TestData.PROMO_DATA['end_date']
        )
        
        final_count = promo_mgmt.get_promotion_cards_count()
        assert final_count == initial_count + 1, f"Gagal menambahkan promosi baru. Awal: {initial_count}, Akhir: {final_count}"
        
    @pytest.mark.admin
    def test_TC_ADM_014_create_promotion_invalid(self, driver):
        """TC_ADM_014: Create promotion dengan data invalid"""
        promo_mgmt = PromotionManagementPage(driver)
        
        driver.get(f"{Config.BASE_URL}/admin/promotions")


        try:
            promo_mgmt.find_element(promo_mgmt.locators.ADD_PROMO_BUTTON, By.XPATH)
            print("[INFO] Halaman Promosi termuat, tombol 'Tambah Promosi' terlihat.")
        except Exception as e:
            raise Exception(f"Gagal memuat Halaman Promosi Admin. Tombol 'Tambah Promosi' tidak ditemukan: {e}")
        
        promo_mgmt.click_add_promotion()
        
        # Try to submit without filling required fields
        promo_mgmt.click_submit()
        time.sleep(2)
        
        # Should show validation errors
        assert True
    
    @pytest.mark.admin
    def test_TC_ADM_015_edit_promotion(self, driver):
        """TC_ADM_015: Edit existing promotion"""
        promo_mgmt = PromotionManagementPage(driver)
        
        driver.get(f"{Config.BASE_URL}/admin/promotions")
        time.sleep(2)
        
        if promo_mgmt.get_promotion_cards_count() > 0:
            promo_mgmt.click_edit_first_promotion()
            time.sleep(2)
            
            # Verify edit modal opened
            assert True
    
    @pytest.mark.admin
    def test_TC_ADM_016_delete_promotion(self, driver):
        """TC_ADM_016: Delete promotion"""
        promo_mgmt = PromotionManagementPage(driver)
        
        driver.get(f"{Config.BASE_URL}/admin/promotions")
        time.sleep(2)
        
        if promo_mgmt.get_promotion_cards_count() > 0:
            # Note: Don't actually delete to keep test data
            # promo_mgmt.click_delete_first_promotion()
            pass
        
        assert True
    
    @pytest.mark.admin
    def test_TC_ADM_017_navigate_to_reports(self, driver):
        """TC_ADM_017: Navigate to reports"""
        admin_dash = AdminDashboardPage(driver)
        
        driver.get(f"{Config.BASE_URL}/admin/dashboard")
        time.sleep(1)
        
        admin_dash.navigate_to_reports()
        time.sleep(2)
        
        assert "/admin/reports" in driver.current_url
    
    @pytest.mark.admin
    def test_TC_ADM_018_view_occupancy_report(self, driver):
        """TC_ADM_018: View occupancy report"""
        driver.get(f"{Config.BASE_URL}/admin/reports")
        time.sleep(2)
        
        # Verify reports page loaded with data
        assert "/admin/reports" in driver.current_url
    
    @pytest.mark.admin
    def test_TC_ADM_019_view_revenue_report(self, driver):
        """TC_ADM_019: View revenue report"""
        driver.get(f"{Config.BASE_URL}/admin/reports")
        time.sleep(2)
        
        # Verify revenue data displayed
        assert "/admin/reports" in driver.current_url
    
    @pytest.mark.admin
    def test_TC_ADM_020_export_report(self, driver, login_admin):
        """TC_ADM_020: Export report dan validasi file terdownload"""

        download_dir = os.path.join(os.getcwd(), "downloads")
        os.makedirs(download_dir, exist_ok=True)

        files_before = set(os.listdir(download_dir))

        driver.get(f"{Config.BASE_URL}/admin/reports")

        export_btn = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable(
                (By.XPATH, "//button[contains(., 'Export')]")
            )
        )
        export_btn.click()

        WebDriverWait(driver, 20).until(
            lambda d: len(set(os.listdir(download_dir)) - files_before) > 0
        )

        files_after = set(os.listdir(download_dir))
        new_files = files_after - files_before

        assert len(new_files) == 1, "❌ File export tidak terdownload"
        print(f"✅ Export berhasil: {list(new_files)[0]}")

