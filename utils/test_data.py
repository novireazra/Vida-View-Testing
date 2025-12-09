from datetime import datetime, timedelta

class TestData:
    # User Credentials
    VALID_ADMIN = {
        'email': 'admin@vidaview.com',
        'password': 'admin123'
    }
    
    VALID_OWNER = {
        'email': 'owner@vidaview.com',
        'password': 'owner123'
    }
    
    VALID_TENANT = {
        'email': 'tenant@vidaview.com',
        'password': 'tenant123'
    }
    
    # Invalid Credentials
    INVALID_EMAIL = 'invalid@test.com'
    INVALID_PASSWORD = 'wrongpassword'
    
    # Registration Data
    VALID_REGISTRATION = {
        'username': 'testuser123',
        'email': 'testuser@test.com',
        'password': 'Password123',
        'full_name': 'Test User Full Name',
        'phone': '081234567890',
        'birth_date': '1995-01-01',
        'address': 'Jl. Test No. 123, Jakarta'
    }
    
    # Booking Data
    BOOKING_DATA = {
        'start_date': (datetime.now() + timedelta(days=7)).strftime("%Y-%m-%d"),
        'end_date': (datetime.now() + timedelta(days=7+180)).strftime("%Y-%m-%d"),
        'notes': 'Test booking untuk testing selenium'
    }
    
    # Promotion Data
    PROMO_DATA = {
        'code': 'TESTPROMO2024',
        'title': 'Test Promo Discount',
        'type': 'percent',
        'value': 10,
        'start_date': datetime.now().strftime("%Y-%m-%d"),
        'end_date': (datetime.now() + timedelta(days=30)).strftime("%Y-%m-%d")
    }
    
    # Unit Data
    UNIT_DATA = {
        'unit_number': 'A-101',
        'unit_type': 'Studio',
        'bedrooms': 1,
        'bathrooms': 1,
        'size': 35,
        'floor': 1,
        'price': 5000000,
        'deposit': 5000000,
        'description': 'Unit studio untuk testing automation'
    }
    
    # Search Keywords
    SEARCH_KEYWORDS = {
        'valid': 'Studio',
        'invalid': 'xxxxxxxx'
    }
    
    # Validation Messages
    VALIDATION_MESSAGES = {
        'required_field': 'wajib diisi',
        'invalid_email': 'email tidak valid',
        'password_mismatch': 'Password tidak cocok',
        'invalid_phone': 'nomor telepon tidak valid',
        'age_restriction': 'minimal 18 tahun'
    }