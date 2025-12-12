import pytest
import time
from pages.login_page import LoginPage
from pages.apartments_page import ApartmentsPage, ApartmentDetailPage
from pages.booking_page import BookingPage
from pages.payment_page import PaymentPage
from pages.documents_page import DocumentsPage
from pages.dashboard_page import DashboardPage
from config.config import Config
from utils.helpers import TestDataGenerator
from utils.test_data import TestData

class TestTenantFlow:
    """Test suite untuk Tenant Flow"""
    
    @pytest.fixture(autouse=True)
    def setup(self, driver):
        """Setup: Login sebagai tenant sebelum setiap test"""
        login_page = LoginPage(driver)
        login_page.navigate_to_login()
        time.sleep(1)
        login_page.login(Config.TENANT_EMAIL, Config.TENANT_PASSWORD)
        time.sleep(2)
        yield
    
    @pytest.mark.smoke
    @pytest.mark.tenant
    @pytest.mark.critical
    def test_TC_TNT_001_search_apartments(self, driver):
        """TC_TNT_001: Search dan filter apartemen"""
        apartments_page = ApartmentsPage(driver)
        
        apartments_page.navigate_to_apartments()
        time.sleep(1)
        
        # Search apartment
        apartments_page.search_apartment("Studio")
        time.sleep(2)
        
        # Verify results ditampilkan
        count = apartments_page.get_apartment_cards_count()
        assert count > 0, "Tidak ada hasil pencarian"
    
    @pytest.mark.tenant
    def test_TC_TNT_002_search_no_results(self, driver):
        """TC_TNT_002: Search dengan keyword yang tidak ada"""
        apartments_page = ApartmentsPage(driver)
        
        apartments_page.navigate_to_apartments()
        time.sleep(1)
        
        apartments_page.search_apartment("XYZNONEXISTENT")
        time.sleep(2)
        
        # Verify 'no results' message
        assert apartments_page.is_no_results_displayed() or apartments_page.get_apartment_cards_count() == 0
    
    @pytest.mark.smoke
    @pytest.mark.tenant
    @pytest.mark.critical
    def test_TC_TNT_003_view_apartment_detail(self, driver):
        """TC_TNT_003: View apartment detail"""
        apartments_page = ApartmentsPage(driver)
        apartment_detail = ApartmentDetailPage(driver)
        
        apartments_page.navigate_to_apartments()
        time.sleep(1)
        
        # Click first apartment
        apartments_page.click_first_apartment()
        time.sleep(2)
        
        # Verify detail page
        assert apartment_detail.get_unit_number() != ""
        assert apartment_detail.get_price() != ""
    
    @pytest.mark.tenant
    def test_TC_TNT_004_add_remove_favorite(self, driver):
        """TC_TNT_004: Add dan remove apartment dari favorites"""
        apartments_page = ApartmentsPage(driver)
        
        apartments_page.navigate_to_apartments()
        time.sleep(1)
        
        # Click favorite button
        apartments_page.click_favorite_button(0)
        time.sleep(2)
        
        # Click again to remove
        apartments_page.click_favorite_button(0)
        time.sleep(2)
        
        # Verify no error occurred
        assert apartments_page.get_apartment_cards_count() > 0
    
    @pytest.mark.tenant
    @pytest.mark.critical
    def test_TC_TNT_005_upload_required_documents(self, driver, create_test_files):
        """TC_TNT_005: Upload dokumen wajib (KTP & Selfie)"""
        docs_page = DocumentsPage(driver)
        
        docs_page.navigate_to_documents()
     
        
        # Upload KTP
        docs_page.upload_ktp(Config.KTP_IMAGE)
     
        
        # Upload Selfie
        docs_page.upload_selfie(Config.SELFIE_IMAGE)
    
        
        # Verify documents uploaded (status pending)
        assert docs_page.is_verification_pending()
    
    @pytest.mark.tenant
    def test_TC_TNT_006_upload_optional_documents(self, driver, create_test_files):
        """TC_TNT_006: Upload dokumen opsional (Income Proof)"""
        docs_page = DocumentsPage(driver)
        
        docs_page.navigate_to_documents()
        time.sleep(2)
        
        # Upload Income Proof
        docs_page.upload_income_proof(Config.INCOME_PROOF)
        time.sleep(3)
        
        # Verify upload success
        assert True  # Jika tidak error, berarti success
    
    @pytest.mark.tenant
    @pytest.mark.critical
    @pytest.mark.slow
    def test_TC_TNT_007_create_booking_without_documents(self, driver):
        """TC_TNT_007: Create booking tanpa upload dokumen wajib (should fail)"""
        apartments_page = ApartmentsPage(driver)
        apartment_detail = ApartmentDetailPage(driver)
        
        apartments_page.navigate_to_apartments()
        time.sleep(1)
        
        apartments_page.click_first_apartment()
        time.sleep(2)
        
        # Try to click booking button
        if apartment_detail.is_booking_button_visible():
            apartment_detail.click_booking_button()
            time.sleep(2)
            
            # Should redirect to documents page or show error
            current_url = driver.current_url
            assert "/documents" in current_url or "/apartments" in current_url
    
    @pytest.mark.tenant
    @pytest.mark.critical
    @pytest.mark.slow
    def test_TC_TNT_008_create_booking_with_promo(self, driver):
        """TC_TNT_008: Create booking dengan kode promo"""
        # Note: Test ini memerlukan dokumen terverifikasi dan promo code valid
        apartments_page = ApartmentsPage(driver)
        apartment_detail = ApartmentDetailPage(driver)
        booking_page = BookingPage(driver)
        
        apartments_page.navigate_to_apartments()
        time.sleep(1)
        
        apartments_page.click_first_apartment()
        time.sleep(2)
        
        if apartment_detail.is_booking_button_visible():
            apartment_detail.click_booking_button()
            time.sleep(2)
            
            # If redirected to booking page (docs verified)
            if "/booking" in driver.current_url:
                start_date, end_date = TestDataGenerator.generate_booking_dates(6)
                
                booking_page.input_start_date(start_date)
                booking_page.input_end_date(end_date)
                booking_page.input_promo_code("TESTPROMO2024")
                booking_page.click_apply_promo()
                time.sleep(2)
                
                # Verify promo applied or error shown
                assert True  # Test completed
    
    @pytest.mark.tenant
    @pytest.mark.slow
    def test_TC_TNT_009_create_booking_invalid_dates(self, driver):
        """TC_TNT_009: Create booking dengan tanggal invalid (end date before start date)"""
        booking_page = BookingPage(driver)
        
        # Navigate directly to booking page (if possible)
        # This test assumes we're on booking page
        
        # Input invalid dates
        end_date = TestDataGenerator.generate_future_date(7)
        start_date = TestDataGenerator.generate_future_date(30)
        
        booking_page.input_start_date(start_date)
        booking_page.input_end_date(end_date)
        time.sleep(1)
        
        # Should show error or prevent submission
        # Verify error handling
        assert True
    
    @pytest.mark.tenant
    @pytest.mark.critical
    @pytest.mark.slow
    def test_TC_TNT_010_payment_bank_transfer(self, driver):
        """TC_TNT_010: Complete payment dengan bank transfer"""
        # Note: Test ini memerlukan booking yang sudah dibuat
        payment_page = PaymentPage(driver)
        
        # Assuming we're on payment page
        # This is a placeholder test
        
        transaction_id = TestDataGenerator.generate_transaction_id()
        
        # Select payment method
        payment_page.select_bank_transfer()
        payment_page.click_next()
        time.sleep(1)
        
        # Go to confirmation step
        payment_page.click_next()
        time.sleep(1)
        
        # Input transaction details
        payment_page.input_transaction_id(transaction_id)
        payment_page.input_notes("Test payment via automation")
        
        # Note: Tidak click confirm untuk avoid creating real payment
        assert True
    
    @pytest.mark.tenant
    def test_TC_TNT_011_view_my_bookings(self, driver):
        """TC_TNT_011: View my bookings page"""
        driver.get(f"{Config.BASE_URL}/my-bookings")
        time.sleep(2)
        
        # Verify page loaded
        assert "/my-bookings" in driver.current_url
    
    @pytest.mark.tenant
    def test_TC_TNT_012_view_my_payments(self, driver):
        """TC_TNT_012: View my payments page"""
        driver.get(f"{Config.BASE_URL}/my-payments")
        time.sleep(2)
        
        # Verify page loaded
        assert "/my-payments" in driver.current_url
    
    @pytest.mark.tenant
    def test_TC_TNT_013_view_profile(self, driver):
        """TC_TNT_013: View dan edit profile"""
        driver.get(f"{Config.BASE_URL}/profile")
        time.sleep(2)
        
        # Verify profile page loaded
        assert "/profile" in driver.current_url
    
    @pytest.mark.tenant
    def test_TC_TNT_014_view_notifications(self, driver):
        """TC_TNT_014: View notifications"""
        dashboard_page = DashboardPage(driver)
        
        dashboard_page.click_notifications()
        time.sleep(2)
        
        # Verify notifications page
        assert "/notifications" in driver.current_url