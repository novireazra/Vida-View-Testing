from pages.base_page import BasePage
from config.locators import DocumentsPageLocators
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
import time

class DocumentsPage(BasePage):
    def __init__(self, driver):
        super().__init__(driver)
        self.locators = DocumentsPageLocators()
    
    def navigate_to_documents(self):
        """Navigate ke documents page"""
        from config.config import Config
        self.navigate_to(f"{Config.BASE_URL}/tenant/documents")
        self.wait_for_page_load()

        print(f"[DEBUG] Setelah navigasi ke dokumen, URL saat ini: {self.driver.current_url}")
        
        locator = self.locators.UPLOAD_BUTTON
        by = By.XPATH

        try:
        # Gunakan find_element untuk menunggu visibilitas tombol Upload
            self.find_element(locator, by)
        except TimeoutException:
            raise TimeoutException(f"Gagal memuat halaman dokumen. Tombol {locator} tidak ditemukan dalam {Config.EXPLICIT_WAIT} detik.")

    def click_upload_button(self):
        """Click upload document button"""
        locator = self.locators.UPLOAD_BUTTON
        by = By.XPATH
            
        # Coba langsung Force Click (yang sudah mengandung wait_for_element_clickable)
        # Jika force_click gagal (Timeout atau Intercepted), force_click akan mencoba mengatasi.
        try:
                self.force_click(locator, by)
        except TimeoutException: # Gunakan TimeoutException spesifik
                # Jika Force Click gagal (Timeout), coba scroll dan klik lagi
                self.scroll_to_element(locator, by)
                self.force_click(locator, by)
        except Exception as e:
                # Tangani exception lain (misal ElementClickIntercepted)
                print(f"Klik gagal, mencoba scroll dan klik lagi. Error: {e.__class__.__name__}")
                self.scroll_to_element(locator, by)
                self.force_click(locator, by)
                
    
    def select_document_type(self, doc_type):
        """Select document type (id_card, selfie, income, reference)"""
        self.select_dropdown_by_value(self.locators.DOCUMENT_TYPE_SELECT, doc_type)
    
    def upload_file(self, filepath):
        """Upload file"""
        super().upload_file(self.locators.FILE_INPUT, filepath)
        time.sleep(1)
    
    def click_upload_in_modal(self):
        """Click upload button di modal"""
        self.click(self.locators.UPLOAD_MODAL_BUTTON, By.XPATH)
        time.sleep(2)
    
    def is_verification_pending(self):
        """Check apakah verifikasi pending"""
        return self.is_element_visible(self.locators.VERIFICATION_STATUS, timeout=3)
    
    def upload_ktp(self, ktp_path):
        """Upload KTP document"""
        self.click_upload_button()
        self.select_document_type("id_card")
        self.upload_file(ktp_path)
        self.click_upload_in_modal()
    
    def upload_selfie(self, selfie_path):
        """Upload Selfie document"""
        self.click_upload_button()
        self.select_document_type("selfie")
        self.upload_file(selfie_path)
        self.click_upload_in_modal()
    
    def upload_income_proof(self, income_path):
        """Upload Income Proof document"""
        self.click_upload_button()
        self.select_document_type("income")
        self.upload_file(income_path)
        self.click_upload_in_modal()
    
    def click_view_document(self):
        """Click view document button"""
        buttons = self.find_elements(self.locators.VIEW_BUTTON, By.XPATH)
        if buttons:
            buttons[0].click()
            time.sleep(1)
            