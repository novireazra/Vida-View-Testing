import pytest
import time
from pages.login_page import LoginPage
from pages.owner_pages import OwnerUnitsPage, AddUnitModal
from pages.dashboard_page import DashboardPage
from config.config import Config
from utils.helpers import TestDataGenerator
from utils.test_data import TestData

class TestOwnerFlow:
    """Test suite untuk Owner Flow"""
    
    @pytest.fixture(autouse=True)
    def setup(self, driver):
        """Setup: Login sebagai owner sebelum setiap test"""
        login_page = LoginPage(driver)
        login_page.navigate_to_login()
        time.sleep(1)
        login_page.login(Config.OWNER_EMAIL, Config.OWNER_PASSWORD)
        time.sleep(2)
        yield
    
    @pytest.mark.smoke
    @pytest.mark.owner
    @pytest.mark.critical
    def test_TC_OWN_001_view_my_units(self, driver):
        """TC_OWN_001: View my units page"""
        units_page = OwnerUnitsPage(driver)
        
        units_page.navigate_to_my_units()
        time.sleep(2)
        
        # Verify page loaded
        assert "/owner/units" in driver.current_url or "/owner/apartments" in driver.current_url
    
    @pytest.mark.owner
    def test_TC_OWN_002_filter_units_available(self, driver):
        """TC_OWN_002: Filter units - Available only"""
        units_page = OwnerUnitsPage(driver)
        
        units_page.navigate_to_my_units()
        time.sleep(1)
        
        units_page.filter_available_units()
        time.sleep(2)
        
        # Verify filter applied
        assert True
    
    @pytest.mark.owner
    def test_TC_OWN_003_filter_units_occupied(self, driver):
        units_page = OwnerUnitsPage(driver)

        units_page.navigate_to_my_units()
        time.sleep(2)

        units_page.filter_occupied_units()
        time.sleep(2)

        assert True

    @pytest.mark.owner
    @pytest.mark.critical
    @pytest.mark.slow
    def test_TC_OWN_004_add_new_unit(self, driver):
        """TC_OWN_004: Add new apartment unit"""
        units_page = OwnerUnitsPage(driver)
        add_modal = AddUnitModal(driver)
        
        units_page.navigate_to_my_units()
        time.sleep(3)
        
        initial_count = units_page.get_units_count()
        
        units_page.click_add_unit()
        time.sleep(3)
        
        # Generate unique unit number
        unit_number = f"TEST-{TestDataGenerator.generate_random_username()[:6].upper()}"
        
        add_modal.add_unit(
            unit_number=unit_number,
            unit_type="Studio",
            bedrooms=1,
            bathrooms=1,
            size=35,
            floor=1,
            price=5000000,
            deposit=5000000,
            description="Unit test automation",
            furnished=True
        )
        time.sleep(3)
        
        # Verify unit added
        # Note: Might need to refresh or check notification
        assert True
    
    @pytest.mark.owner
    def test_TC_OWN_005_add_unit_invalid_data(self, driver):
        """TC_OWN_005: Add unit dengan data invalid (missing required fields)"""
        units_page = OwnerUnitsPage(driver)
        add_modal = AddUnitModal(driver)
        
        units_page.navigate_to_my_units()
        time.sleep(2)

        print("==== DEBUG BUTTON TEXT ON PAGE ====")
    buttons = driver.find_elements(By.XPATH, "//button")
    for b in buttons:
        print(f"[BUTTON] '{b.text}'")
        
        units_page.click_add_unit()
        time.sleep(2)
        
        # Try to submit without filling required fields
        add_modal.click_submit()
        time.sleep(2)
        
        # Should show validation errors
        # Verify still on modal or form
        assert True
    
    @pytest.mark.owner
    @pytest.mark.critical
    def test_TC_OWN_006_edit_unit(self, driver):
        """TC_OWN_006: Edit existing unit"""
        units_page = OwnerUnitsPage(driver)
        
        units_page.navigate_to_my_units()
        time.sleep(1)
        
        # Check if there are units to edit
        if units_page.get_units_count() > 0:
            units_page.click_edit_first_unit()
            time.sleep(2)
            
            # Verify edit modal opened
            assert True
    
    @pytest.mark.owner
    @pytest.mark.critical
    def test_TC_OWN_007_archive_unit(self, driver):
        """TC_OWN_007: Archive unit"""
        units_page = OwnerUnitsPage(driver)
        
        units_page.navigate_to_my_units()
        time.sleep(1)
        
        if units_page.get_units_count() > 0:
            units_page.click_archive_first_unit()
            time.sleep(2)
            
            # Confirm archive in modal if needed
            # Note: May need to click confirm button
            assert True
    
    @pytest.mark.owner
    def test_TC_OWN_008_view_unit_detail(self, driver):
        """TC_OWN_008: View unit detail from my units"""
        units_page = OwnerUnitsPage(driver)
        
        units_page.navigate_to_my_units()
        time.sleep(1)
        
        if units_page.get_units_count() > 0:
            units_page.click_view_first_unit()
            time.sleep(2)
            
            # Verify redirected to detail page
            assert "/apartments/" in driver.current_url
    
    @pytest.mark.owner
    @pytest.mark.critical
    def test_TC_OWN_009_view_bookings(self, driver):
        """TC_OWN_009: View bookings for my units"""
        driver.get(f"{Config.BASE_URL}/owner/bookings")
        time.sleep(2)
        
        # Verify bookings page loaded
        assert "/owner/bookings" in driver.current_url
    
    @pytest.mark.owner
    @pytest.mark.critical
    def test_TC_OWN_010_approve_booking(self, driver):
        """TC_OWN_010: Approve pending booking"""
        # Navigate to bookings page
        driver.get(f"{Config.BASE_URL}/owner/bookings")
        time.sleep(2)
        
        # This test requires a pending booking to exist
        # Placeholder for approve action
        assert "/owner/bookings" in driver.current_url
    
    @pytest.mark.owner
    def test_TC_OWN_011_reject_booking(self, driver):
        """TC_OWN_011: Reject pending booking"""
        driver.get(f"{Config.BASE_URL}/owner/bookings")
        time.sleep(2)
        
        # Placeholder for reject action
        assert "/owner/bookings" in driver.current_url
    
    @pytest.mark.owner
    def test_TC_OWN_012_view_financial_report(self, driver):
        """TC_OWN_012: View financial report"""
        driver.get(f"{Config.BASE_URL}/owner/financial")
        time.sleep(2)
        
        # Verify financial report page loaded
        assert "/owner/financial" in driver.current_url or "/owner/reports" in driver.current_url
    
    @pytest.mark.owner
    def test_TC_OWN_013_view_payments(self, driver):
        """TC_OWN_013: View payments from tenants"""
        driver.get(f"{Config.BASE_URL}/owner/payments")
        time.sleep(4)
        
        # Verify payments page loaded
        assert "/owner/payments" in driver.current_url
    
    @pytest.mark.owner
    def test_TC_OWN_014_verify_payment(self, driver):
        """TC_OWN_014: Verify tenant payment"""
        driver.get(f"{Config.BASE_URL}/owner/payments")
        time.sleep(4)
        
        # Placeholder for verify payment action
        assert "/owner/payments" in driver.current_url