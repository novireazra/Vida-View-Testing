import os
from pathlib import Path

class Config:
    # Base Configuration
    BASE_URL = "http://localhost:3000"  # Ganti dengan URL frontend Anda
    API_URL = "http://localhost:5001"   # Ganti dengan URL backend Anda
    
    # Browser Configuration
    BROWSER = "chrome"  # chrome, firefox, edge
    HEADLESS = False
    IMPLICIT_WAIT = 10
    EXPLICIT_WAIT = 20
    PAGE_LOAD_TIMEOUT = 30
    
    # Test Data - Credentials
    ADMIN_EMAIL = "noviazzahrah13@gmail.com"
    ADMIN_PASSWORD = "12345678901"
    
    OWNER_EMAIL = "novireazra@gmail.com"
    OWNER_PASSWORD = "12345678"
    
    TENANT_EMAIL = "ramadhaninra23h@student.unhas.ac.id"
    TENANT_PASSWORD = "1234567890"
    
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