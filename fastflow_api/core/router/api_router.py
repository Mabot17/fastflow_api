# ============================================= Start Noted API Router ===================================
# Author : Abdul Rohman Masrifan | masrifan26@gamil.com
# Perhatikan kode titik, ini bisa menjadi masuk ke sub folder 
# - from core.router.users import users
# 1. core = nama folder
# 2. router = nama folder
# 3. users = nama folder
# 4. import users = import (nama file .py)
# ============================================= End Noted API Router ===================================

from fastapi import APIRouter

from core.modules.api_docs import api_docs_router, versi_router
from core.modules.auth import login_router
from core.modules.users.router import users_router
from core.modules.master import (
    produk_barcode_router,
)
from core.modules.wablas import (
    wablas_router,
    # wablas_netsales_router
)

from core.modules.text_to_voice import (
    text_to_voice_router,
)

apiSettings = APIRouter()

# CATATAN include_router():
# - Untuk pengurutan disini bisa dicek file api_metadata.py
# - Jika di api_router.py sudah ditulis tapi belum urut, maka perlu diurutkan dari metadata
# - Di file tsb digunakan memberikan keterangan juga pada router sesuai nama router
# - Di file tsb digunakan untuk mengurutkan berdasarkan data api_router.py
apiSettings.include_router(api_docs_router.routerDocs)
apiSettings.include_router(login_router.routerLogin)
apiSettings.include_router(versi_router.routerVersi)
apiSettings.include_router(users_router.routerUser)

# API Route Master
apiSettings.include_router(produk_barcode_router.routerProdukBarcode, prefix="/master")

# Start router Eksternal atau pihak ke 3
apiSettings.include_router(wablas_router.routerWablas)
apiSettings.include_router(text_to_voice_router.routerTextToVoice)

