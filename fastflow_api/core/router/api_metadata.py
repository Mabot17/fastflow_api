# ============================================= Start Noted JSON ===================================
# Author : Abdul Rohman Masrifan | masrifan26@gamil.com
# 1. Nilai Konstanta Digunakan untuk menyimpan API metadata, deskripsi, versi dll
# 2. Untuk deskripsi jelas di api_router.py
# ============================================= END Noted JSON ===================================

# Title Versi 
TITLE_API = "FASTFLOW API"
VERSI_API = "0.1.0"

# NOTED : 
# 1. tags_metadata >> Digunakan sebagai urutan dalam dokumentasi
# 2. Untuk urutan berdasarkan kode `Name` di file api_router.py
# 3. Disini digunakan untuk memberikan informasi/deskripsi tambahan per router API per modul
TAGS_METADATA_API = [
    {
        "name": "Version",
        "description": """
    Versi API
        """,
    },
    {
        "name": "Authentication",
        "description": """
    Untuk register bisa pakai API POST /users (create users)
    
    Login untuk mendapatkan access token.
    Sebagian besar endpoint hanya bisa diakses dengan menggunakan access token.
        """,
    },
    {"name": "Sistem - Users", "description": """
    User akan digunakan untuk masuk system dan akses API, Akses Menu akan diberikan berdasarkan user_group_id

    Setiap User akan memiliki karyawan:
     - Penggunaan Karyawan digunakan untuk pembuatan, persetujuan dokumen, dll
        """
    },
    {
        "name": "Master - Produk Barcode",
        "description": """
    Master - Data Produk Dengan Barcode
        """
    },
    {
        "name": "WABLAS - Tools Pengiriman Whatsapp",
        "description": """
    API Untuk Pengiriman Whatsapp ke group berupa text, image, document, File Lainnya
        """
    },
    {
        "name": "Text To Voice",
        "description": """
    API Untuk Mengubah text to audio
        """
    }
]


# Noted 
# Deskripsion metadata API
DESCRIPTION_API = """
FastFlow: Simplifying Complexity, Enhancing Performance.
"""