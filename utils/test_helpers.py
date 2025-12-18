"""
Helper functions for test setup and teardown
"""
import requests
from config.config import Config


class TestSetupHelper:
    """Helper class untuk setup data test"""

    @staticmethod
    def verify_tenant_documents_via_api(tenant_email):
        """
        Verifikasi dokumen tenant melalui API admin
        Memerlukan admin credentials

        Returns:
            bool: True jika berhasil, False jika gagal
        """
        try:
            # Login as admin
            login_response = requests.post(
                f"{Config.API_URL}/auth/login",
                json={
                    "email": Config.ADMIN_EMAIL,
                    "password": Config.ADMIN_PASSWORD
                }
            )

            if login_response.status_code != 200:
                print(f"[ERROR] Admin login failed: {login_response.status_code}")
                return False

            admin_token = login_response.json().get('token')

            # Get user ID by email
            headers = {"Authorization": f"Bearer {admin_token}"}
            users_response = requests.get(
                f"{Config.API_URL}/admin/users",
                headers=headers,
                params={"search": tenant_email}
            )

            if users_response.status_code != 200:
                print(f"[ERROR] Get users failed: {users_response.status_code}")
                return False

            users = users_response.json().get('users', [])
            tenant_user = next((u for u in users if u['email'] == tenant_email), None)

            if not tenant_user:
                print(f"[ERROR] Tenant with email {tenant_email} not found")
                return False

            user_id = tenant_user['id']

            # Verify documents
            verify_response = requests.post(
                f"{Config.API_URL}/admin/users/{user_id}/verify-documents",
                headers=headers
            )

            if verify_response.status_code in [200, 201]:
                print(f"[SUCCESS] Dokumen tenant {tenant_email} berhasil diverifikasi")
                return True
            else:
                print(f"[ERROR] Verify documents failed: {verify_response.status_code}")
                print(f"Response: {verify_response.text}")
                return False

        except Exception as e:
            print(f"[ERROR] Exception during document verification: {e}")
            return False

    @staticmethod
    def check_tenant_document_status(tenant_email, tenant_password):
        """
        Cek status dokumen tenant

        Returns:
            dict: Status dokumen (has_ktp, has_selfie, is_verified, document_verified_at)
        """
        try:
            # Login as tenant
            login_response = requests.post(
                f"{Config.API_URL}/auth/login",
                json={
                    "email": tenant_email,
                    "password": tenant_password
                }
            )

            if login_response.status_code != 200:
                return None

            token = login_response.json().get('token')

            # Get profile
            headers = {"Authorization": f"Bearer {token}"}
            profile_response = requests.get(
                f"{Config.API_URL}/users/profile",
                headers=headers
            )

            if profile_response.status_code != 200:
                return None

            profile = profile_response.json()

            return {
                'has_ktp': profile.get('id_card_photo') is not None,
                'has_selfie': profile.get('selfie_photo') is not None,
                'is_verified': profile.get('document_verified_at') is not None,
                'document_verified_at': profile.get('document_verified_at')
            }

        except Exception as e:
            print(f"[ERROR] Exception checking document status: {e}")
            return None


def ensure_tenant_documents_verified():
    """
    Decorator untuk memastikan dokumen tenant sudah diverifikasi sebelum test
    """
    def decorator(test_func):
        def wrapper(*args, **kwargs):
            # Check document status
            status = TestSetupHelper.check_tenant_document_status(
                Config.TENANT_EMAIL,
                Config.TENANT_PASSWORD
            )

            if not status:
                print("[ERROR] Tidak bisa cek status dokumen tenant")
                return

            print(f"[INFO] Status dokumen tenant: {status}")

            # If not verified, try to verify
            if not status['is_verified']:
                print("[INFO] Dokumen belum diverifikasi, mencoba verifikasi via API...")
                success = TestSetupHelper.verify_tenant_documents_via_api(Config.TENANT_EMAIL)

                if not success:
                    print("[WARNING] Gagal verifikasi dokumen via API. Test mungkin gagal.")
                    print("[INFO] Silakan verifikasi dokumen secara manual:")
                    print(f"  1. Login sebagai admin ({Config.ADMIN_EMAIL})")
                    print("  2. Buka Admin Panel > Users")
                    print(f"  3. Cari user: {Config.TENANT_EMAIL}")
                    print("  4. Klik tombol 'Verifikasi Dokumen'")

            # Run the test
            return test_func(*args, **kwargs)

        return wrapper
    return decorator
