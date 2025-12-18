from selenium.webdriver.common.by import By

class LoginPageLocators:
    EMAIL_INPUT = (By.XPATH, "//input[@name='email']")
    PASSWORD_INPUT = (By.CSS_SELECTOR, "input[name='password']")
    LOGIN_BUTTON = (By.CSS_SELECTOR, "button[type='submit']")
    REGISTER_LINK = (By.CSS_SELECTOR, "a[href='/register']")
    ERROR_MESSAGE = (By.CSS_SELECTOR, ".bg-red-50")
    REMEMBER_CHECKBOX = (By.CSS_SELECTOR, "input#remember-me")

class RegisterPageLocators:
    USERNAME_INPUT = (By.CSS_SELECTOR, "input[name='username']")
    EMAIL_INPUT = (By.CSS_SELECTOR, "input[name='email']")
    PASSWORD_INPUT = (By.CSS_SELECTOR, "input[name='password']")
    CONFIRM_PASSWORD_INPUT = (By.CSS_SELECTOR, "input[name='confirmPassword']")
    FULL_NAME_INPUT = (By.CSS_SELECTOR, "input[name='full_name']")
    PHONE_INPUT = (By.CSS_SELECTOR, "input[name='phone']")
    BIRTH_DATE_INPUT = (By.CSS_SELECTOR, "input[name='birth_date']")
    BIRTH_DATE_ERROR_MESSAGE = (By.CSS_SELECTOR, ".text-red-500")
    ADDRESS_INPUT = (By.CSS_SELECTOR, "input[name='address']")
    ROLE_TENANT_BUTTON = (By.XPATH, "//button[contains(., 'Penyewa')]")
    ROLE_OWNER_BUTTON = (By.XPATH, "//button[contains(., 'Pemilik')]")
    TERMS_CHECKBOX = (By.CSS_SELECTOR, "input#terms")
    REGISTER_BUTTON = (By.CSS_SELECTOR, "button[type='submit']")
    LOGIN_LINK = (By.CSS_SELECTOR, "a[href='/login']")

class NavbarLocators:
    LOGO = (By.CSS_SELECTOR, "img[alt='Vida View Logo']")
    BERANDA_LINK = (By.CSS_SELECTOR, "a[href='/']")
    UNIT_LINK = (By.CSS_SELECTOR, "a[href='/apartments']")
    PROFILE_BUTTON = (By.CSS_SELECTOR, ".flex.items-center.space-x-2")
    NOTIFICATION_BUTTON = (By.CSS_SELECTOR, "a[href='/notifications']")
    NOTIFICATION_BADGE = (By.CSS_SELECTOR, ".bg-red-600.rounded-full")
    LOGOUT_BUTTON = (By.XPATH, "//button[contains(text(), 'Keluar')]")
    DASHBOARD_LINK = (By.XPATH, "//a[contains(text(), 'Dashboard')]")

class ApartmentsPageLocators:
    SEARCH_INPUT = (By.CSS_SELECTOR, "input[placeholder*='Cari']")
    FILTER_STATUS = (By.CSS_SELECTOR, "select")
    APARTMENT_CARD = (By.CSS_SELECTOR, "a[href^='/apartments/']")
    APARTMENT_CARD_ALT = (By.CSS_SELECTOR, ".grid > a")
    APARTMENT_CARD_CONTAINER = (By.CSS_SELECTOR, ".bg-white.rounded-lg.shadow-md")
    APARTMENT_TITLE = (By.CSS_SELECTOR, "h3.font-semibold")
    APARTMENT_PRICE = (By.CSS_SELECTOR, ".text-purple-600.font-bold")
    VIEW_DETAIL_BUTTON = (By.XPATH, "//button[contains(text(), 'Lihat Detail')]")
    FAVORITE_BUTTON = (By.CSS_SELECTOR, "button[title='Add to favorites']")
    PAGINATION_NEXT = (By.XPATH, "//button[contains(text(), 'Next')]")
    NO_RESULTS = (By.XPATH, "//p[contains(text(), 'Tidak Ada Apartemen')]")

class ApartmentDetailLocators:
    UNIT_NUMBER = (By.CSS_SELECTOR, "h1.text-3xl.font-bold")
    UNIT_TYPE = (By.CSS_SELECTOR, ".text-lg.text-gray-600")
    PRICE = (By.CSS_SELECTOR, ".text-3xl.font-bold.text-purple-600")
    BOOKING_BUTTON = (By.XPATH, "//button[contains(text(), 'Booking Sekarang')]")
    CONTACT_OWNER_BUTTON = (By.XPATH, "//button[contains(text(), 'Hubungi Pemilik')]")
    FAVORITE_BUTTON = (By.XPATH, "//button[contains(., 'Favorit')]")
    BACK_BUTTON = (By.XPATH, "//button[contains(text(), 'Kembali')]")
    IMAGE_GALLERY = (By.CSS_SELECTOR, ".swiper-slide img")
    BEDROOMS = (By.XPATH, "//p[contains(text(), 'Kamar Tidur')]/following-sibling::p")
    BATHROOMS = (By.XPATH, "//p[contains(text(), 'Kamar Mandi')]/following-sibling::p")
    FACILITIES_LIST = (By.CSS_SELECTOR, ".grid.gap-3")

class BookingPageLocators:
    START_DATE_INPUT = (By.CSS_SELECTOR, "input[name='start_date']")
    END_DATE_INPUT = (By.CSS_SELECTOR, "input[name='end_date']")
    NOTES_TEXTAREA = (By.CSS_SELECTOR, "textarea[name='notes']")
    PROMO_CODE_INPUT = (By.CSS_SELECTOR, "input[placeholder*='promosi']")
    APPLY_PROMO_BUTTON = (By.XPATH, "//button[contains(text(), 'Terapkan')]")
    REMOVE_PROMO_BUTTON = (By.XPATH, "//button[contains(text(), 'Hapus')]")
    SUMMARY_TOTAL = (By.CSS_SELECTOR, ".text-3xl.font-bold")
    SUBMIT_BUTTON = (By.CSS_SELECTOR, "button[type='submit']")
    BACK_BUTTON = (By.XPATH, "//button[contains(text(), 'Kembali')]")
    APPLIED_PROMO_CODE = (By.CSS_SELECTOR, ".bg-green-50 .font-semibold")

class PaymentPageLocators:
    BANK_TRANSFER_OPTION = (By.XPATH, "//div[contains(text(), 'Bank Transfer')]")
    CREDIT_CARD_OPTION = (By.XPATH, "//div[contains(text(), 'Kartu Kredit')]")
    EWALLET_OPTION = (By.XPATH, "//div[contains(text(), 'E-Wallet')]")
    TRANSACTION_ID_INPUT = (By.CSS_SELECTOR, "input[placeholder*='transaksi']")
    RECEIPT_UPLOAD = (By.CSS_SELECTOR, "input#receipt-upload")
    NOTES_INPUT = (By.CSS_SELECTOR, "textarea[placeholder*='Catatan']")
    CONFIRM_BUTTON = (By.XPATH, "//button[contains(text(), 'Konfirmasi Pembayaran')]")
    NEXT_BUTTON = (By.XPATH, "//button[contains(text(), 'Lanjutkan')]")
    PREVIOUS_BUTTON = (By.XPATH, "//button[contains(text(), 'Kembali')]")

class DocumentsPageLocators:
    UPLOAD_KTP_BUTTON = (By.XPATH, "//button[contains(., 'Upload') and contains(., 'Kartu Identitas')]")
    UPLOAD_SELFIE_BUTTON = (By.XPATH, "//button[contains(., 'Upload') and contains(., 'Selfie')]")
    UPLOAD_INCOME_BUTTON = (By.XPATH, "//button[contains(., 'Upload') and contains(., 'Bukti Penghasilan')]")
    UPLOAD_REFERENCE_BUTTON = (By.XPATH, "//button[contains(., 'Upload') and contains(., 'Surat Referensi')]")
    UPLOAD_BUTTON = (By.XPATH, "//button[contains(., 'Upload') and contains(@class, 'w-full')]")
    DOCUMENT_TYPE_SELECT = (By.CSS_SELECTOR, "select")
    FILE_INPUT = (By.CSS_SELECTOR, "input#document-upload")
    UPLOAD_MODAL_BUTTON = (By.XPATH, "//button[contains(text(), 'Upload Dokumen') and not(contains(., 'Kartu')) and not(contains(., 'Selfie'))]")
    VIEW_BUTTON = (By.XPATH, "//button[contains(., 'Lihat')]")
    VERIFICATION_STATUS = (By.CSS_SELECTOR, ".bg-green-100, .bg-yellow-100")
    KTP_CARD = (By.XPATH, "//h3[normalize-space(text())='Kartu Identitas']")
    SELFIE_CARD = (By.XPATH, "//h3[contains(text(), 'Foto Selfie')]")

class DashboardLocators:
    STATS_CARD = (By.CSS_SELECTOR, ".bg-white.rounded-lg.shadow-md")
    WELCOME_MESSAGE = (By.CSS_SELECTOR, ".bg-gradient-to-r")
    BOOKING_CARD = (By.CSS_SELECTOR, ".space-y-4 > div")
    QUICK_ACTION = (By.XPATH, "//a[contains(@class, 'hover:shadow-lg')]")

class AdminDashboardLocators:
    USERS_LINK = (By.CSS_SELECTOR, "a[href='/admin/users']")
    BOOKINGS_LINK = (By.CSS_SELECTOR, "a[href='/admin/bookings']")
    PAYMENTS_LINK = (By.CSS_SELECTOR, "a[href='/admin/payments']")
    PROMOTIONS_LINK = (By.CSS_SELECTOR, "a[href='/admin/promotions']")
    REPORTS_LINK = (By.CSS_SELECTOR, "a[href='/admin/reports']")
    STATS_CARD = (By.CSS_SELECTOR, ".grid.gap-6 > div")

class UserManagementLocators:
    SEARCH_INPUT = (By.CSS_SELECTOR, "input[name='search']")
    ROLE_FILTER = (By.CSS_SELECTOR, "select[name='role']")
    STATUS_FILTER = (By.CSS_SELECTOR, "select[name='status']")
    USER_ROW = (By.CSS_SELECTOR, "tbody tr")
    EDIT_BUTTON = (By.CSS_SELECTOR, "button[title='Edit']")
    DELETE_BUTTON = (By.CSS_SELECTOR, "button[title='Hapus']")
    VERIFY_BUTTON = (By.CSS_SELECTOR, "button[title='Verifikasi Dokumen']")
    VIEW_DOCS_BUTTON = (By.CSS_SELECTOR, "button[title='Lihat Dokumen']")
    SAVE_BUTTON = (By.XPATH, "//button[contains(text(), 'Simpan')]")
    CONFIRM_VERIFY_BUTTON = (By.XPATH, "//button[contains(text(), 'Verifikasi') and not(contains(@title, 'Verifikasi'))]")
    CONFIRM_DELETE_BUTTON = (By.XPATH, "//button[contains(text(), 'Hapus')]")

class PromotionLocators:
    ADD_PROMO_BUTTON = (By.XPATH, "//button[contains(., 'Tambah Promosi')]")
    PROMO_CODE_INPUT = (By.CSS_SELECTOR, "input[placeholder*='LEBARAN']")
    PROMO_TITLE_INPUT = (By.CSS_SELECTOR, "input[placeholder*='Diskon']")
    PROMO_DESCRIPTION_TEXTAREA = (By.CSS_SELECTOR, "textarea[placeholder*='Deskripsi']")
    PROMO_TYPE_SELECT = (By.CSS_SELECTOR, "select")
    PROMO_VALUE_INPUT = (By.CSS_SELECTOR, "input[type='number']")
    PROMO_USAGE_LIMIT_INPUT = (By.CSS_SELECTOR, "input[placeholder*='batas']")
    START_DATE_INPUT = (By.XPATH, "(//input[@type='date'])[1]") # Input tanggal ke-1
    END_DATE_INPUT = (By.XPATH, "(//input[@type='date'])[2]")   # Input tanggal ke-2
    ACTIVE_CHECKBOX = (By.CSS_SELECTOR, "input[type='checkbox']")
    SUBMIT_BUTTON = (By.XPATH, "//button[@type='submit' and (contains(text(), 'Tambah') or contains(text(), 'Perbarui'))]")
    CANCEL_BUTTON = (By.XPATH, "//button[contains(text(), 'Batal')]")
    EDIT_BUTTON = (By.XPATH, "//button[contains(., 'Edit')]")
    DELETE_BUTTON = (By.XPATH, "//button[contains(., 'Hapus')]")
    PROMO_CARD = (By.CSS_SELECTOR, ".bg-white.rounded-xl.shadow-md")

class OwnerUnitsLocators:
    # Menggunakan translate untuk case-insensitive text matching di XPath 1.0
    ADD_UNIT_BUTTON = (By.XPATH, "//button[contains(translate(., 'TAMBAH', 'tambah'), 'tambah')]")
    UNIT_CARD = (By.CSS_SELECTOR, ".relative > div")
    VIEW_BUTTON = (By.CSS_SELECTOR, "button[title='Lihat Detail']")
    EDIT_BUTTON = (By.CSS_SELECTOR, "button[title='Edit']")
    DELETE_BUTTON = (By.CSS_SELECTOR, "button[title='Hapus Unit']")
    ARCHIVE_BUTTON = (By.CSS_SELECTOR, "button[title='Arsipkan']")
    FILTER_ALL = (By.XPATH, "//button[contains(text(), 'Semua')]")
    FILTER_AVAILABLE = (By.XPATH, "//button[contains(text(), 'Tersedia')]")
    FILTER_OCCUPIED = (By.XPATH, "//button[contains(text(), 'Terisi')]")

class AddUnitModalLocators:
    UNIT_NUMBER_INPUT = (By.CSS_SELECTOR, "input[name='name']")  # Updated based on actual form
    UNIT_TYPE_SELECT = (By.CSS_SELECTOR, "select")
    BEDROOMS_INPUT = (By.CSS_SELECTOR, "input[name='bedrooms']")
    BATHROOMS_INPUT = (By.CSS_SELECTOR, "input[name='bathrooms']")
    SIZE_INPUT = (By.CSS_SELECTOR, "input[name='size']")  # Updated
    FLOOR_INPUT = (By.CSS_SELECTOR, "input[name='floor']")  # Updated
    PRICE_INPUT = (By.CSS_SELECTOR, "input[name='monthly_rent']")  # Updated
    DEPOSIT_INPUT = (By.CSS_SELECTOR, "input[name='deposit']")  # Updated
    DESCRIPTION_TEXTAREA = (By.CSS_SELECTOR, "textarea")
    FURNISHED_CHECKBOX = (By.CSS_SELECTOR, "input[name='furnished']")  # Updated
    PHOTO_UPLOAD = (By.CSS_SELECTOR, "input[type='file']")
    SUBMIT_BUTTON = (By.XPATH, "//button[contains(text(), 'Tambah')]")
    CANCEL_BUTTON = (By.XPATH, "//button[contains(text(), 'Batal')]")