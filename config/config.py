import os
from pathlib import Path

class Config:
    # Base Configuration
    BASE_URL = "http://localhost:3000"  # Ganti dengan URL frontend Anda
    API_URL = "http://localhost:5000"   # Ganti dengan URL backend Anda
    
    # Browser Configuration
    BROWSER = "chrome"  # chrome, firefox, edge
    HEADLESS = False
    IMPLICIT_WAIT = 10
    EXPLICIT_WAIT = 20
    PAGE_LOAD_TIMEOUT = 30
    
    # Test Data - Credentials
    ADMIN_EMAIL = "vidaview@admin.com"
    ADMIN_PASSWORD = "reskares9"
    
    OWNER_EMAIL = "testing@pemilik.com"
    OWNER_PASSWORD = "reskares9"
    
    TENANT_EMAIL = "testing@penyewa.com"
    TENANT_PASSWORD = "reskares9"
    
    # New User Registration Data
    NEW_USER_PREFIX = "testuser"
    NEW_USER_PASSWORD = "Password123"
    
    # Paths
    ROOT_DIR = Path(__file__).parent.parent
    SCREENSHOTS_DIR = ROOT_DIR / "screenshots"
    REPORTS_DIR = ROOT_DIR / "reports"
    TEST_FILES_DIR = ROOT_DIR / "test_files"
    
    # Create directories if not exist
    SCREENSHOTS_DIR.mkdir(exist_ok=True)
    REPORTS_DIR.mkdir(exist_ok=True)
    TEST_FILES_DIR.mkdir(exist_ok=True)
    
    # Test Files
    KTP_IMAGE = TEST_FILES_DIR / "sample_ktp.jpg"
    SELFIE_IMAGE = TEST_FILES_DIR / "sample_selfie.jpg"
    INCOME_PROOF = TEST_FILES_DIR / "sample_income.pdf"