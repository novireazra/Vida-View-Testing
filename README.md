📋 TUTORIAL LENGKAP: Menjalankan Test Vida-View-Testing
📂 Ringkasan Project
Project ini adalah automated testing untuk aplikasi Vida View (sistem manajemen apartemen) menggunakan:
Framework: Selenium 4 + Pytest
Browser: Chrome (default) atau Firefox
Total Test: 72 test cases
User Roles: Admin, Owner (Pemilik), Tenant (Penyewa)
1️⃣ PERSIAPAN AWAL
Step 1: Install Dependencies
Pastikan Python sudah terinstall (Python 3.8+), kemudian install semua library yang dibutuhkan:
cd "/Users/macbookprorezka/Library/Mobile Documents/com~apple~CloudDocs/SEMESTER 5/PROYEK PERANGKAT LUNAK/Vida-View-Testing"

pip install -r requirements.txt
Library yang akan terinstall:
selenium - Web automation
pytest - Test framework
pytest-html - HTML reporting
pytest-xdist - Parallel execution
webdriver-manager - Auto download webdriver
Faker, openpyxl, pandas - Utilities
Step 2: Konfigurasi
Pastikan aplikasi Vida View sudah berjalan di:
Frontend: http://localhost:3000
Backend: http://localhost:5000
Anda bisa mengubah konfigurasi di config/config.py:
BASE_URL = "http://localhost:3000"
API_URL = "http://localhost:5000"
User credentials yang digunakan (sesuai config/config.py):
Admin: vidaview@admin.com / reskares9
Owner: testing@pemilik.com / reskares9
Tenant: testing@penyewa.com / reskares9
2️⃣ CARA MENJALANKAN TEST
A. Menjalankan SEMUA Test
# Menjalankan semua test di semua file
pytest

# Menjalankan dengan output verbose (detail)
pytest -v

# Menjalankan dengan output yang lebih detail
pytest -vv

# Menjalankan dengan menampilkan print statements
pytest -s

# Menjalankan dengan kombinasi verbose + print
pytest -v -s
B. Menjalankan SATU FILE Test
# Contoh: Menjalankan semua test di test_admin_flow.py
pytest tests/test_admin_flow.py -v

# Contoh: Menjalankan test_authentication.py
pytest tests/test_authentication.py -v

# Contoh: Menjalankan test_tenant_flow.py
pytest tests/test_tenant_flow.py -v

# Contoh: Menjalankan test_owner_flow.py
pytest tests/test_owner_flow.py -v

# Contoh: Menjalankan test_validations.py
pytest tests/test_validations.py -v
C. Menjalankan SATU TEST CASE Spesifik
Ada 2 cara:
Cara 1: Menggunakan nama class dan function
# Format: pytest tests/nama_file.py::NamaClass::nama_function -v

# Contoh 1: Test login admin
pytest tests/test_admin_flow.py::TestAdminFlow::test_TC_ADM_001_view_admin_dashboard -v

# Contoh 2: Test create promotion
pytest tests/test_admin_flow.py::TestAdminFlow::test_TC_ADM_013_create_promotion -v

# Contoh 3: Test search user
pytest tests/test_admin_flow.py::TestAdminFlow::test_TC_ADM_003_search_user -v
Cara 2: Menggunakan keyword (-k)
# Mencari test yang mengandung kata tertentu
pytest -k "view_admin_dashboard" -v

# Mencari test yang mengandung "promotion"
pytest -k "promotion" -v

# Mencari test yang mengandung "create"
pytest -k "create" -v
D. Menjalankan Test Berdasarkan MARKER
Project ini menggunakan markers untuk kategori test:
# Test smoke (critical tests)
pytest -m smoke -v

# Test admin saja
pytest -m admin -v

# Test owner saja
pytest -m owner -v

# Test tenant saja
pytest -m tenant -v

# Test authentication
pytest -m authentication -v

# Test validation
pytest -m validation -v

# Test critical saja
pytest -m critical -v

# Kombinasi markers (admin DAN critical)
pytest -m "admin and critical" -v

# Test admin ATAU tenant
pytest -m "admin or tenant" -v
3️⃣ OPSI LANJUTAN
A. Generate HTML Report
# Generate report HTML
pytest --html=reports/report.html --self-contained-html

# Generate dengan verbose
pytest -v --html=reports/report.html --self-contained-html
Report akan tersimpan di folder reports/
B. Menjalankan Test Secara Paralel
# Menjalankan test dengan 2 worker (paralel)
pytest -n 2

# Menjalankan test dengan 4 worker
pytest -n 4

# Auto-detect jumlah CPU
pytest -n auto
⚠️ Note: Hati-hati dengan paralel, bisa menyebabkan konflik data
C. Mode Headless (Tanpa Browser Window)
Edit config/config.py:
HEADLESS = True  # Browser akan berjalan di background
Atau jalankan langsung:
pytest -v  # Browser headless akan aktif jika HEADLESS=True
D. Stop Saat Test Pertama Gagal
pytest -x  # Stop saat test pertama fail

pytest --maxfail=3  # Stop setelah 3 test fail
E. Menjalankan Test yang Gagal Saja (Re-run Failures)
# Run pertama
pytest --lf  # Last Failed - hanya test yang gagal terakhir kali

pytest --ff  # Failed First - jalankan yang gagal dulu, baru yang lain
4️⃣ CONTOH PRAKTIS
Scenario 1: Testing Admin Flow
# 1. Test dashboard admin
pytest tests/test_admin_flow.py::TestAdminFlow::test_TC_ADM_001_view_admin_dashboard -v -s

# 2. Test user management
pytest tests/test_admin_flow.py::TestAdminFlow::test_TC_ADM_002_navigate_to_users -v -s
pytest tests/test_admin_flow.py::TestAdminFlow::test_TC_ADM_003_search_user -v -s

# 3. Test promotion management
pytest tests/test_admin_flow.py::TestAdminFlow::test_TC_ADM_013_create_promotion -v -s

# 4. Jalankan semua test admin
pytest tests/test_admin_flow.py -v
Scenario 2: Testing Authentication
# Test semua authentication
pytest tests/test_authentication.py -v

# Test login admin saja
pytest -k "login_admin" -v

# Test login dengan marker
pytest -m authentication -v
Scenario 3: Quick Smoke Test
# Hanya test yang penting (marked dengan @pytest.mark.smoke)
pytest -m smoke -v --html=reports/smoke_report.html
5️⃣ STRUKTUR FILE TEST
File test yang ada:
File	Test Cases	Fokus
test_admin_flow.py	20 tests	Admin dashboard, user management, bookings, payments, promotions, reports
test_authentication.py	~15 tests	Login & registration untuk semua role
test_validations.py	~15 tests	Form validation & error handling
test_owner_flow.py	~15 tests	Owner dashboard, unit management, listings
test_tenant_flow.py	~20 tests	Apartment search, booking, payment, documents
6️⃣ TROUBLESHOOTING
Problem 1: ChromeDriver Error
# Uninstall dan install ulang webdriver-manager
pip uninstall webdriver-manager
pip install webdriver-manager
Problem 2: Aplikasi Belum Jalan
Pastikan frontend & backend sudah running:
# Check apakah port sudah digunakan
lsof -i :3000  # Frontend
lsof -i :5000  # Backend
Problem 3: Test Timeout
Edit timeout di config/config.py:
IMPLICIT_WAIT = 20  # Increase dari 10
EXPLICIT_WAIT = 30  # Increase dari 20
PAGE_LOAD_TIMEOUT = 60  # Increase dari 30
Problem 4: Element Not Found
Jalankan dengan mode non-headless untuk debug:
HEADLESS = False  # di config.py
7️⃣ COMMAND CHEAT SHEET
# Basic
pytest                                  # Run all tests
pytest -v                              # Verbose output
pytest -v -s                           # Verbose + print statements

# Specific tests
pytest tests/test_admin_flow.py        # One file
pytest tests/test_admin_flow.py::TestAdminFlow::test_TC_ADM_001_view_admin_dashboard  # One test

# Markers
pytest -m smoke                        # Smoke tests only
pytest -m admin                        # Admin tests only
pytest -m "admin and critical"         # Combined markers

# Reporting
pytest --html=reports/report.html      # HTML report
pytest -n auto                         # Parallel execution

# Control
pytest -x                              # Stop on first failure
pytest --lf                            # Run last failed
pytest --maxfail=3                     # Stop after 3 failures
🎯 REKOMENDASI
Untuk Development:
pytest -v -s --maxfail=1
Untuk CI/CD:
pytest -v --html=reports/report.html -n auto
Untuk Debug:
pytest tests/test_admin_flow.py::TestAdminFlow::test_TC_ADM_001_view_admin_dashboard -v -s
Apakah ada test case spesifik yang ingin Anda jalankan? Atau ada yang perlu saya jelaskan lebih detail? 😊