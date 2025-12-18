# TC_ADM_013 & TC_ADM_014 - Fix Summary

## Status: ✅ RESOLVED

Both test cases are now **PASSING** successfully!

## Tests Fixed
- **TC_ADM_013**: Create new promotion ✅
- **TC_ADM_014**: Create promotion with invalid data ✅

## Test Results

```bash
# TC_ADM_013
pytest tests/test_admin_flow.py::TestAdminFlow::test_TC_ADM_013_create_promotion -v -s
Result: PASSED
- Initial promotion count: 2
- Final promotion count: 3 ✅
- Promotion successfully created with all fields filled

# TC_ADM_014
pytest tests/test_admin_flow.py::TestAdminFlow::test_TC_ADM_014_create_promotion_invalid -v -s
Result: PASSED
- Form validation working correctly
- Empty form submission prevented ✅
```

## Root Cause

The issue was that **React controlled components** were not detecting value changes when using standard Selenium methods or basic JavaScript value assignment.

### Why It Failed Before

1. **Direct value assignment** (`element.value = 'x'`) doesn't work with React
2. React overrides the native input value setter
3. React's `onChange` handlers only trigger on specific events
4. Standard `send_keys()` unreliable for date/number inputs

### What Was Happening

- Values were being set in the DOM
- But React's internal state wasn't updating
- Form validation saw empty fields
- Submission failed or values weren't saved

## The Solution

Use React's **native value setter descriptor** with proper event dispatching:

```javascript
const input = arguments[0];
const value = arguments[1];

// Get React's native value setter
const nativeInputValueSetter = Object.getOwnPropertyDescriptor(
    window.HTMLInputElement.prototype,
    'value'
).set;

// Use native setter to update value
nativeInputValueSetter.call(input, value);

// Dispatch event so React detects the change
const event = new Event('input', { bubbles: true });
input.dispatchEvent(event);
```

## Files Changed

### 1. config/locators.py (lines 128-141)
**What Changed:** Updated locators to match exact frontend placeholders

```python
# Before
PROMO_CODE_INPUT = "input[placeholder*='Kode']"
PROMO_TITLE_INPUT = "input[placeholder*='Judul']"

# After
PROMO_CODE_INPUT = "input[placeholder*='LEBARAN']"  # "Contoh: LEBARAN2025"
PROMO_TITLE_INPUT = "input[placeholder*='Diskon']"  # "Contoh: Diskon Spesial..."
```

### 2. pages/admin_pages.py (lines 136-270)
**What Changed:** Rewrote ALL input methods to use React value setter

Methods updated:
- `input_promo_code()` - Text input with uppercase conversion
- `input_promo_title()` - Text input
- `select_promo_type()` - Select dropdown (uses HTMLSelectElement)
- `input_promo_value()` - Number input
- `input_start_date()` - Date input with 'change' event
- `input_end_date()` - Date input with 'change' event

**Key Implementation:**
```python
def input_promo_code(self, code):
    import time
    try:
        code_input = self.find_element(self.locators.PROMO_CODE_INPUT)

        # React value setter approach
        self.driver.execute_script("""
            const input = arguments[0];
            const value = arguments[1];
            const nativeInputValueSetter = Object.getOwnPropertyDescriptor(
                window.HTMLInputElement.prototype, 'value'
            ).set;
            nativeInputValueSetter.call(input, value);
            const event = new Event('input', { bubbles: true });
            input.dispatchEvent(event);
        """, code_input, code.upper())

        time.sleep(0.3)
        print(f"[DEBUG] Set promo code: {code.upper()}")
    except Exception as e:
        print(f"[ERROR] Failed to input promo code: {e}")
        raise
```

## Technical Details

### For Text Inputs (code, title, value)
- Use `HTMLInputElement.prototype.value` setter
- Dispatch `'input'` event with bubbling
- React's onChange handler triggers on 'input' event

### For Select Dropdowns (type)
- Use `HTMLSelectElement.prototype.value` setter
- Dispatch `'change'` event with bubbling
- React's onChange handler triggers on 'change' event

### For Date Inputs (start_date, end_date)
- Use `HTMLInputElement.prototype.value` setter
- Dispatch `'change'` event (not 'input')
- Date inputs use 'change' event in React
- Format: YYYY-MM-DD (e.g., '2025-12-17')

## Validation Rules (from frontend)

The frontend validates:
1. **Code**: Required, max 20 chars, uppercase alphanumeric + underscore/dash
2. **Title**: Required
3. **Value**: Required, must be > 0, max 100 if percentage
4. **Start Date**: Required
5. **End Date**: Required, must be after start date
6. **Usage Limit**: Optional, must be >= 0 if provided

All these validations now work correctly because React state is properly updated!

## How to Run Tests

```bash
# Individual tests (recommended)
cd vida_view_testing

# TC_ADM_013 - Create promotion
pytest tests/test_admin_flow.py::TestAdminFlow::test_TC_ADM_013_create_promotion -v -s

# TC_ADM_014 - Invalid promotion
pytest tests/test_admin_flow.py::TestAdminFlow::test_TC_ADM_014_create_promotion_invalid -v -s
```

## Expected Output

### TC_ADM_013 Success:
```
[TEST] Navigating to promotions...
[TEST] Current URL: http://localhost:3000/admin/promotions
[TEST] Add promotion button found
[TEST] Initial promotion count: 2

[DEBUG] Creating promotion: PROMORBS1X3
[DEBUG] Step 1: Clicking add promotion button...
[INFO] Modal Tambah Promosi berhasil terbuka.
[DEBUG] Step 2: Inputting code: PROMORBS1X3
[DEBUG] Set promo code: PROMORBS1X3
[DEBUG] Step 3: Inputting title: Test Automation Promo
[DEBUG] Set promo title: Test Automation Promo
[DEBUG] Step 4: Selecting type: percent
[DEBUG] Set promo type: percent
[DEBUG] Step 5: Inputting value: 15
[DEBUG] Set promo value: 15
[DEBUG] Step 6: Inputting start date: 2025-12-17
[DEBUG] Input start date: 2025-12-17
[DEBUG] Step 7: Inputting end date: 2026-01-16
[DEBUG] Input end date: 2026-01-16
[DEBUG] Step 8: Checking active checkbox...
[DEBUG] Step 9: Clicking submit...
[DEBUG] Promotion creation steps completed

[TEST] Promotion creation completed
[TEST] Final promotion count: 3

✅ PASSED
```

## Key Learnings

1. **React Controlled Components**: Standard DOM manipulation doesn't work
2. **Event Dispatching Critical**: React relies on synthetic events
3. **Native Setters Required**: Must use descriptor to bypass React's override
4. **Different Events for Different Inputs**: 'input' vs 'change' events matter
5. **Bubbling Important**: Events must bubble up for React to catch them

## Future Reference

This same approach should be used for **any React form testing** where controlled components are involved. The pattern is:

1. Find the element
2. Get native value setter descriptor
3. Call setter with new value
4. Dispatch appropriate event (input/change) with bubbling
5. Wait for React to update

## Related Documentation

- [React Forms Documentation](https://react.dev/reference/react-dom/components/input)
- [React Controlled Components](https://react.dev/learn/sharing-state-between-components#controlled-and-uncontrolled-components)
- TROUBLESHOOTING_TC_ADM_13.md (comprehensive troubleshooting guide)
- debug_promotion_test.py (interactive debugging script)
