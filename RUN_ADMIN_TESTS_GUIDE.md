# Panduan Menjalankan Admin Flow Tests

Dokumen ini menjelaskan cara menjalankan semua test cases admin flow sekaligus.

## Prerequisites

Sebelum menjalankan tests, pastikan:

### 1. Backend dan Frontend Running
```bash
# Terminal 1 - Backend
cd backend
python run.py
# Backend should run on http://localhost:5000

# Terminal 2 - Frontend
cd frontend
npm start
# Frontend should run on http://localhost:3000
```

### 2. Database Siap
- Database PostgreSQL sudah disetup
- Ada data user admin dengan credentials:
  - Email: `admin@vidaview.com` (atau sesuai Config.ADMIN_EMAIL)
  - Password: `admin123` (atau sesuai Config.ADMIN_PASSWORD)

### 3. Dependencies Installed
```bash
cd vida_view_testing
pip install -r requirements.txt
```

---

## Cara Menjalankan Tests

### Option 1: Menggunakan Script (Recommended)

#### Windows:
```cmd
cd vida_view_testing
run_all_admin_tests.bat
```

#### Linux/Mac:
```bash
cd vida_view_testing
./run_all_admin_tests.sh
```

Script ini akan:
- Menjalankan semua 19 test cases
- Menampilkan output detail di console
- Generate HTML report di `reports/admin_flow_report.html`

---

### Option 2: Command Line Manual

#### Menjalankan Semua Tests:
```bash
cd vida_view_testing
pytest tests/test_admin_flow.py -v
```

#### Menjalankan dengan Output Detail:
```bash
pytest tests/test_admin_flow.py -v -s
```

#### Menjalankan dengan HTML Report:
```bash
pytest tests/test_admin_flow.py -v --html=reports/admin_flow_report.html --self-contained-html
```

#### Menjalankan Tests Tertentu Saja:
```bash
# Run hanya critical tests
pytest tests/test_admin_flow.py -v -m critical

# Run hanya smoke tests
pytest tests/test_admin_flow.py -v -m smoke

# Run specific test
pytest tests/test_admin_flow.py::TestAdminFlow::test_TC_ADM_013_create_promotion -v -s
```

---

## Test Cases yang Akan Dijalankan

| No | Test Case | Description | Status |
|----|-----------|-------------|--------|
| 1 | TC_ADM_001 | View admin dashboard | ✅ Working |
| 2 | TC_ADM_002 | Navigate to users | ✅ Working |
| 3 | TC_ADM_003 | Search user | ✅ Working |
| 4 | TC_ADM_004 | Filter users by role | ✅ Working |
| 5 | TC_ADM_005 | Filter users by status | ✅ Working |
| 6 | TC_ADM_006 | View user documents | ✅ Working |
| 7 | TC_ADM_007 | Verify user documents | ✅ Fixed |
| 8 | TC_ADM_008 | Edit user | ✅ Fixed |
| 9 | TC_ADM_009 | Navigate to bookings | ⏭️ Skipped (feature not implemented) |
| 10 | TC_ADM_010 | Navigate to payments | ✅ Working |
| 11 | TC_ADM_011 | Verify payment | ✅ Working |
| 12 | TC_ADM_012 | Navigate to promotions | ✅ Working |
| 13 | TC_ADM_013 | Create promotion | ✅ Fixed (React value setter) |
| 14 | TC_ADM_014 | Create promotion invalid | ✅ Fixed |
| 15 | TC_ADM_015 | Edit promotion | ✅ Working |
| 16 | TC_ADM_016 | Delete promotion | ✅ Fixed |
| 17 | TC_ADM_017 | Navigate to reports | ✅ Working |
| 18 | TC_ADM_018 | View occupancy report | ✅ Working |
| 19 | TC_ADM_019 | View revenue report | ✅ Working |
| 20 | TC_ADM_020 | Export report | ✅ Fixed |

**Total: 19 tests** (18 active, 1 skipped)

---

## Expected Output

### Successful Run:
```
======================== test session starts =========================
platform win32 -- Python 3.13.3, pytest-7.4.3, pluggy-1.6.0
rootdir: C:\Users\novi\Documents\PPL\vida-view-apartment-website\vida_view_testing
collected 19 items

tests/test_admin_flow.py::TestAdminFlow::test_TC_ADM_001_view_admin_dashboard PASSED [ 5%]
tests/test_admin_flow.py::TestAdminFlow::test_TC_ADM_002_navigate_to_users PASSED [10%]
tests/test_admin_flow.py::TestAdminFlow::test_TC_ADM_003_search_user PASSED [15%]
...
tests/test_admin_flow.py::TestAdminFlow::test_TC_ADM_020_export_report PASSED [100%]

==================== 18 passed, 1 skipped in 180.45s ====================
```

---

## Troubleshooting

### Error: "Failed to load page - got login"
**Penyebab:** Session expired atau browser baru dibuka setiap test

**Solusi:** Tests menggunakan fixture `setup` yang login otomatis. Jika error persist:
1. Check credentials di `config/config.py`
2. Verify admin user exists di database
3. Check backend running properly

### Error: "Element not found"
**Penyebab:** Frontend belum fully loaded atau locator salah

**Solusi:**
1. Increase wait times di test
2. Check frontend console untuk errors
3. Check screenshot di `screenshots/` folder

### Error: "No promotions/users available"
**Penyebab:** Database kosong

**Solusi:**
1. Run seed data script
2. Create test data manually
3. For TC_ADM_016, run TC_ADM_013 first to create promotion

### Tests Running Too Slow
**Solusi:**
```bash
# Run tests in parallel (requires pytest-xdist)
pytest tests/test_admin_flow.py -v -n 3  # Run 3 tests in parallel
```

**Note:** Some tests may fail when run in parallel due to shared state (e.g., creating/deleting promotions)

---

## Generated Reports

### HTML Report
- Location: `reports/admin_flow_report.html`
- Includes: Test results, duration, error messages
- Open in browser to view

### Screenshots
- Location: `screenshots/`
- Generated on test failure
- Named by test case (e.g., `tc_adm_007_verify_failed.png`)

---

## Tips untuk Testing yang Efektif

### 1. Run Tests Incrementally
Jika ada failure, debug satu per satu:
```bash
# Run failed test individually
pytest tests/test_admin_flow.py::TestAdminFlow::test_TC_ADM_XXX -v -s
```

### 2. Use Markers
Run subset tests:
```bash
# Critical tests only
pytest tests/test_admin_flow.py -v -m critical

# Smoke tests only
pytest tests/test_admin_flow.py -v -m smoke

# Skip slow tests
pytest tests/test_admin_flow.py -v -m "not slow"
```

### 3. Check Logs
- Console output shows detailed [TEST], [DEBUG], [INFO], [ERROR] messages
- Use `-s` flag to see all print statements
- Screenshots saved in `screenshots/` folder

### 4. Clean State
Beberapa tests modify data (create, delete). Untuk consistent results:
- Run tests in specific order
- Reset database state sebelum test suite
- Or accept that some tests may fail on second run

---

## Common Test Sequences

### Full Suite (Recommended Order):
```bash
pytest tests/test_admin_flow.py -v
```

### Only Navigation Tests:
```bash
pytest tests/test_admin_flow.py -v -k "navigate"
```

### Only CRUD Tests:
```bash
pytest tests/test_admin_flow.py -v -k "create or edit or delete"
```

### Quick Smoke Test:
```bash
pytest tests/test_admin_flow.py -v -m smoke
```

---

## CI/CD Integration

Untuk CI/CD pipeline, gunakan command:
```bash
pytest tests/test_admin_flow.py -v --tb=short --html=reports/admin_flow_report.html --self-contained-html --junitxml=reports/junit.xml
```

Ini akan generate:
- HTML report untuk viewing
- JUnit XML untuk CI tools (Jenkins, GitLab CI, etc.)

---

## Need Help?

Jika masih ada issues:

1. **Check dokumentasi fix:**
   - TC_ADM_013_014_FIX_SUMMARY.md - Promotion tests
   - TC_ADM_007_008_016_020_FIX_SUMMARY.md - Other fixed tests
   - TROUBLESHOOTING_TC_ADM_13.md - Detailed troubleshooting

2. **Run debug script:**
   ```bash
   python debug_promotion_test.py  # For promotion-related issues
   ```

3. **Check screenshots:**
   ```bash
   ls screenshots/tc_adm_*.png  # View all test screenshots
   ```

4. **Verify environment:**
   ```bash
   # Backend
   curl http://localhost:5000/health

   # Frontend
   curl http://localhost:3000
   ```

---

## Summary Commands

```bash
# Quick start (Windows)
cd vida_view_testing
run_all_admin_tests.bat

# Quick start (Linux/Mac)
cd vida_view_testing
./run_all_admin_tests.sh

# Manual run with report
pytest tests/test_admin_flow.py -v --html=reports/admin_flow_report.html

# Run specific test with debug
pytest tests/test_admin_flow.py::TestAdminFlow::test_TC_ADM_013_create_promotion -v -s
```

Good luck with testing! 🚀
