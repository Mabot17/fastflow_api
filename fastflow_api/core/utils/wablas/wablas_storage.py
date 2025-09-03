# ============================================= Start Noted Router ===================================
# Author : Abdul Rohman Masrifan | https://fastflow.pybot.cloud/ | masrifan26@gmail.com
# 1. Untuk menyimpan API url satusehat
# 2. Tidak disimpan di ENV kenapa?, supaya pertimbangan testing swagger lebih dinamis
# ============================================= END Noted Router ===================================
from enum import Enum
from ...config import WABLAS_TOKEN, WABLAS_SECRET_KEY

class ApiWablasStorage(str, Enum):
    WABLAS_URL = "https://solo.wablas.com/api"

    @staticmethod
    def get_auth_key() -> str:
        """Mengembalikan token otorisasi dalam format WABLAS_TOKEN.WABLAS_SECRET_KEY."""
        if not WABLAS_TOKEN or not WABLAS_SECRET_KEY:
            return None
        return f"{WABLAS_TOKEN}.{WABLAS_SECRET_KEY}"
