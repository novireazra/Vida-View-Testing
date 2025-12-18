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
        target_url = f"{Config.BASE_URL}/my-documents"

        print(f"[DEBUG] Mencoba navigasi ke: {target_url}")
        self.navigate_to(target_url)
        self.wait_for_page_load()
        time.sleep(2)  # Tambahkan wait untuk memastikan redirect selesai

        current_url = self.driver.current_url
        print(f"[DEBUG] Setelah navigasi ke dokumen, URL saat ini: {current_url}")

        # Check jika ada redirect
        if current_url != target_url:
            print(f"[WARNING] Terjadi redirect dari {target_url} ke {current_url}")
            # Coba ambil page title untuk debug
            print(f"[DEBUG] Page title: {self.driver.title}")

        locator = self.locators.UPLOAD_BUTTON
        by = By.XPATH

        try:
            # Gunakan find_element untuk menunggu visibilitas tombol Upload
            self.find_element(locator, by)
        except TimeoutException:
            # Tambahkan screenshot untuk debugging
            screenshot_path = self.take_screenshot("documents_page_error.png")
            print(f"[DEBUG] Screenshot disimpan di: {screenshot_path}")
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

        # Wait for modal to open
        time.sleep(2)
                
    
    def select_document_type(self, doc_type):
        """Select document type (id_card, selfie, income, reference)"""
        self.select_dropdown_by_value(self.locators.DOCUMENT_TYPE_SELECT, doc_type)
    
    def upload_file(self, filepath):
        """Upload file - file input is hidden, so use direct approach"""
        from selenium.webdriver.common.by import By
        # File input is hidden, so we can't use visibility check
        # Use driver.find_element directly instead of self.find_element
        try:
            element = self.driver.find_element(By.CSS_SELECTOR, self.locators.FILE_INPUT)
            element.send_keys(str(filepath))
            time.sleep(1)
        except Exception as e:
            print(f"[ERROR] Gagal upload file: {e}")
            # Take screenshot for debugging
            self.take_screenshot("upload_file_error.png")
            raise
    
    def click_upload_in_modal(self):
        """Click upload button di modal"""
        # Use force_click to handle modal backdrop interception
        self.force_click(self.locators.UPLOAD_MODAL_BUTTON, By.XPATH)
        time.sleep(2)
    
    def is_verification_pending(self):
        """Check apakah verifikasi pending"""
        return self.is_element_visible(self.locators.VERIFICATION_STATUS, timeout=3)
    
    def upload_ktp(self, ktp_path):
        """Upload KTP document"""
        # Click specific KTP upload button
        locator = self.locators.UPLOAD_KTP_BUTTON
        by = By.XPATH
        try:
            self.force_click(locator, by)
        except Exception as e:
            print(f"[ERROR] Gagal klik tombol upload KTP: {e}")
            self.scroll_to_element(locator, by)
            self.force_click(locator, by)
        time.sleep(2)  # Wait for modal

        # Select document type
        self.select_document_type("id_card")
        time.sleep(1)

        # Upload file
        self.upload_file(ktp_path)
        time.sleep(1)

        # Click upload in modal
        self.click_upload_in_modal()

    def upload_selfie(self, selfie_path):
        """Upload Selfie document"""
        # Click specific Selfie upload button
        locator = self.locators.UPLOAD_SELFIE_BUTTON
        by = By.XPATH
        try:
            self.force_click(locator, by)
        except Exception as e:
            print(f"[ERROR] Gagal klik tombol upload Selfie: {e}")
            self.scroll_to_element(locator, by)
            self.force_click(locator, by)
        time.sleep(2)  # Wait for modal

        # Select document type
        self.select_document_type("selfie")
        time.sleep(1)

        # Upload file
        self.upload_file(selfie_path)
        time.sleep(1)

        # Click upload in modal
        self.click_upload_in_modal()

    def upload_income_proof(self, income_path):
        """Upload Income Proof document"""
        # Click specific Income upload button
        locator = self.locators.UPLOAD_INCOME_BUTTON
        by = By.XPATH
        try:
            self.force_click(locator, by)
        except Exception as e:
            print(f"[ERROR] Gagal klik tombol upload Income: {e}")
            self.scroll_to_element(locator, by)
            self.force_click(locator, by)
        time.sleep(2)  # Wait for modal

        # Select document type
        self.select_document_type("income")
        time.sleep(1)

        # Upload file
        self.upload_file(income_path)
        time.sleep(1)

        # Click upload in modal
        self.click_upload_in_modal()
    
    def click_view_document(self):
        """Click view document button"""
        buttons = self.find_elements(self.locators.VIEW_BUTTON, By.XPATH)
        if buttons:
            buttons[0].click()
            time.sleep(1)
            