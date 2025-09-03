# models/master/__init__.py
"""
============================================= Start Noted Global check ===================================
Author : Abdul Rohman Masrifan | https://fastflow.pybot.cloud/ | masrifan26@gmail.com
1. Inisialisasi model master supaya dikenali lebih cepat
2. Dipakai untuk global pemanggilan model & mempersingkat pemanggilan & merapikan modularitas
3. Pemanggilan akan seperti bawah ini, tanpa lengkap :
    from router.sinkronisasi_data import sinkronisasi_data_router
============================================= END Noted Global check ===================================
"""

from .router import (
    text_to_voice_router,
)