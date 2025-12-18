# Troubleshooting Guide: TC_ADM_13 Create Promotion

## ✅ RESOLVED - Test Now Passing

**Solution:** Used React's native value setter with proper event dispatching.

TC_ADM_013 and TC_ADM_014 are now working correctly! The key fix was using React's internal value setter descriptor instead of direct value assignment.

## Perbaikan yang Sudah Dilakukan

### 1. ✅ Locators Updated
**File:** `config/locators.py` lines 121-131

```python
# OLD (SALAH - terlalu umum)
PROMO_CODE_INPUT = "input[placeholder*='Kode']"
PROMO_TITLE_INPUT = "input[placeholder*='Judul']"

# NEW (BENAR - spesifik)
PROMO_CODE_INPUT = "input[placeholder*='LEBARAN']"  # Match "Contoh: LEBARAN2025"
PROMO_TITLE_INPUT = "input[placeholder*='Diskon']"  # Match "Contoh: Diskon..."
```

### 2. ✅ JavaScript Input Methods with React Value Setter
**File:** `pages/admin_pages.py` lines 136-270

Semua input sekarang menggunakan React's native value setter:
```javascript
const input = arguments[0];
const value = arguments[1];
const nativeInputValueSetter = Object.getOwnPropertyDescriptor(
    window.HTMLInputElement.prototype, 'value'
).set;
nativeInputValueSetter.call(input, value);
const event = new Event('input', { bubbles: true });
input.dispatchEvent(event);
```

Methods updated:
- `input_promo_code()` - React value setter + 'input' event
- `input_promo_title()` - React value setter + 'input' event
- `select_promo_type()` - React value setter + 'change' event (for select)
- `input_promo_value()` - React value setter + 'input' event
- `input_start_date()` - React value setter + 'change' event
- `input_end_date()` - React value setter + 'change' event

**Kenapa React Value Setter?**
- React controlled components override native value setter
- Direct `element.value = x` doesn't trigger React's onChange handler
- Must use `Object.getOwnPropertyDescriptor` to get native setter
- Then dispatch event so React detects the change
- This ensures React state updates properly

### 3. ✅ Detailed Debug Logging
**File:** `pages/admin_pages.py` lines 214-264

Method `create_promotion()` sekarang print di setiap step:
```python
[DEBUG] Creating promotion: CODE123
[DEBUG] Step 1: Clicking add promotion button...
[DEBUG] Step 2: Inputting code: CODE123
[DEBUG] Set promo code: CODE123
[DEBUG] Step 3: Inputting title: Test Promo
[DEBUG] Set promo title: Test Promo
# ... dst
```

## Cara Debug Jika Masih Error

### Step 1: Jalankan dengan Debug Output
```bash
cd vida_view_testing
pytest tests/test_admin_flow.py::TestAdminFlow::test_TC_ADM_013_create_promotion -v -s
```

**Perhatikan output:**
- Di step mana test berhenti?
- Error message apa yang muncul?
- Screenshot apa yang di-generate?

### Step 2: Identifikasi Error Type

#### Error Type A: "Add Promo Button Not Found"
```
[ERROR] Add promotion button not found: Message: no such element
```

**Solusi:**
1. Verify URL: `http://localhost:3000/admin/promotions`
2. Manual check: Apakah button "Tambah Promosi" ada?
3. Check login: Apakah masih login sebagai admin?
4. Screenshot: `tc_adm_013_button_not_found.png`

#### Error Type B: "Modal Inputs Not Found"
```
[ERROR] Failed to input promo code: Message: no such element
```

**Solusi:**
1. Modal mungkin tidak terbuka
2. Check method `click_add_promotion()` berhasil atau tidak
3. Tambah wait time setelah click button:
   ```python
   self.click_add_promotion()
   time.sleep(3)  # Increase dari 2 ke 3
   ```
4. Screenshot: `tc_adm_013_create_failed.png`

#### Error Type C: "Date Input Error"
```
[ERROR] Start date input not found
atau
End date input not found
```

**Solusi:**
1. Check berapa banyak date inputs di halaman:
   ```python
   date_inputs = driver.find_elements(By.CSS_SELECTOR, "input[type='date']")
   print(f"Found {len(date_inputs)} date inputs")
   ```
2. Harus ada minimal 2 date inputs
3. Jika kurang dari 2, berarti modal tidak fully loaded

#### Error Type D: "Validation Error on Submit"
```
Toast error: "Mohon lengkapi semua field yang wajib diisi"
```

**Solusi:**
1. Check field mana yang kosong
2. Run debug script untuk manual check:
   ```bash
   python debug_promotion_test.py
   ```
3. Pause sebelum submit dan inspect form values

#### Error Type E: "Count Not Increased"
```
AssertionError: Gagal menambahkan promosi baru. Awal: 5, Akhir: 5
```

**Solusi:**
1. Promo mungkin tidak ter-submit
2. Atau promo code duplicate (pakai yang sudah ada)
3. Check network tab di browser untuk response API
4. Verify TestDataGenerator.generate_promo_code() generates unique code

### Step 3: Manual Testing

1. **Manual Create Promo:**
   - Login sebagai admin
   - Buka http://localhost:3000/admin/promotions
   - Klik "Tambah Promosi"
   - Fill form manual:
     - Code: TEST2024
     - Title: Test Promo
     - Type: Persentase
     - Value: 15
     - Start: (pilih tanggal hari ini)
     - End: (pilih tanggal 30 hari ke depan)
   - Klik "Tambah"
   - Apakah berhasil?

2. **Jika Manual Berhasil tapi Test Gagal:**
   - Issue ada di automation code
   - Run debug script untuk compare

3. **Jika Manual Gagal:**
   - Issue ada di frontend/backend
   - Check console errors
   - Check network tab untuk API errors

## Common Issues & Solutions

### Issue 1: Promo Code Already Exists
```python
# Fix: Ensure unique code generation
promo_code = f"AUTO{datetime.now().strftime('%Y%m%d%H%M%S')}"
```

### Issue 2: Modal Slow to Open
```python
# Fix: Increase wait time after click
self.click_add_promotion()
time.sleep(3)  # From 2 to 3 seconds
```

### Issue 3: React Not Detecting Input Changes
```python
# Fix: Already implemented - using JavaScript with dispatchEvent
self.driver.execute_script(
    "arguments[0].value = arguments[1]; "
    "arguments[0].dispatchEvent(new Event('input', { bubbles: true }));",
    element, value
)
```

### Issue 4: Date Format Wrong
```python
# Correct format: YYYY-MM-DD
start_date = "2024-12-17"  # ✅
start_date = "17/12/2024"  # ❌
start_date = "12-17-2024"  # ❌
```

## Checklist Sebelum Run Test

- [ ] Backend running di http://localhost:5000
- [ ] Frontend running di http://localhost:3000
- [ ] Login admin work: noviazzahrah13@gmail.com / 12345678901
- [ ] Page /admin/promotions accessible
- [ ] Button "Tambah Promosi" visible
- [ ] Modal opens when button clicked
- [ ] All form fields visible in modal
- [ ] TestData.PROMO_DATA has correct format dates

## Debug Commands

```bash
# 1. Run test with full output
pytest tests/test_admin_flow.py::TestAdminFlow::test_TC_ADM_013_create_promotion -v -s

# 2. Run debug script
python debug_promotion_test.py

# 3. Check screenshots
ls screenshots/tc_adm_013*.png

# 4. Check if promotion was created (check backend DB)
# Or check via browser: http://localhost:3000/admin/promotions
```

## Expected Success Output

```
[TEST] Navigating to promotions...
[TEST] Current URL: http://localhost:3000/admin/promotions
[TEST] Add promotion button found
[TEST] Initial promotion count: 5

[DEBUG] Creating promotion: AUTO20241217120000
[DEBUG] Step 1: Clicking add promotion button...
[INFO] Modal Tambah Promosi berhasil terbuka.

[DEBUG] Step 2: Inputting code: AUTO20241217120000
[DEBUG] Set promo code: AUTO20241217120000

[DEBUG] Step 3: Inputting title: Test Automation Promo
[DEBUG] Set promo title: Test Automation Promo

[DEBUG] Step 4: Selecting type: percent
[DEBUG] Set promo type: percent

[DEBUG] Step 5: Inputting value: 15
[DEBUG] Set promo value: 15

[DEBUG] Step 6: Inputting start date: 2024-12-17
[DEBUG] Input start date: 2024-12-17

[DEBUG] Step 7: Inputting end date: 2025-01-16
[DEBUG] Input end date: 2025-01-16

[DEBUG] Step 8: Checking active checkbox...
[DEBUG] Step 9: Clicking submit...
[DEBUG] Promotion creation steps completed

[TEST] Promotion creation completed
[TEST] Final promotion count: 6

✅ PASSED
```

## Contact for Help

Jika masih error setelah troubleshooting:
1. Copy full error output
2. Attach screenshots dari folder screenshots/
3. Describe apa yang sudah dicoba
