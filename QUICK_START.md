# Quick Start - Admin Tests

## 🚀 Cara Tercepat Menjalankan Semua Admin Tests

### Windows:
```cmd
cd vida_view_testing
run_all_admin_tests.bat
```

### Linux/Mac:
```bash
cd vida_view_testing
./run_all_admin_tests.sh
```

---

## ⚠️ Checklist Sebelum Run Tests

- [ ] Backend running di `http://localhost:5000`
- [ ] Frontend running di `http://localhost:3000`
- [ ] Database PostgreSQL aktif
- [ ] Admin user exists (admin@vidaview.com / admin123)

---

## 📊 Alternative Commands

### Run semua tests:
```bash
pytest tests/test_admin_flow.py -v
```

### Run dengan output detail:
```bash
pytest tests/test_admin_flow.py -v -s
```

### Run dengan HTML report:
```bash
pytest tests/test_admin_flow.py -v --html=reports/admin_flow_report.html
```

### Run specific test:
```bash
pytest tests/test_admin_flow.py::TestAdminFlow::test_TC_ADM_013_create_promotion -v -s
```

---

## 📝 Test Summary

**Total Tests:** 19
- ✅ **18 Active tests**
- ⏭️ **1 Skipped** (TC_ADM_009 - bookings page not implemented)

**Test Categories:**
- Navigation: 5 tests
- User Management: 5 tests
- Promotions: 4 tests
- Payments: 2 tests
- Reports: 3 tests

---

## 🐛 Quick Troubleshooting

### Tests redirect to login:
→ Check admin credentials in `config/config.py`

### Element not found errors:
→ Check screenshots in `screenshots/` folder

### No data available errors:
→ Seed database with test data

---

## 📚 Full Documentation

Untuk panduan lengkap, lihat: **[RUN_ADMIN_TESTS_GUIDE.md](RUN_ADMIN_TESTS_GUIDE.md)**

---

## ⚡ Quick Tips

1. **Run tests secara berurutan** untuk hasil terbaik
2. **Check report HTML** di `reports/admin_flow_report.html`
3. **View screenshots** di `screenshots/` saat ada error
4. **Use `-s` flag** untuk melihat debug output detail

Happy Testing! 🎉
