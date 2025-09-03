# ============================================= Start Noted JSON ===================================
# Author : Abdul Rohman Masrifan | masrifan26@gamil.com
# 1. Response return wajib JSON/dict supaya bisa diolah kembali di router
# ============================================= END Noted JSON ===================================
from sqlalchemy.orm import Session, aliased
from ...models.info.info_model import InfoModel

import logging

async def json_info(db: Session, info_data_row: InfoModel) -> dict:
    try:
        return_info = {
            "info_id": info_data_row.info_id,
            "info_nama": info_data_row.info_nama,
            "info_alamat": info_data_row.info_alamat,
            "info_notelp": info_data_row.info_notelp,
            "info_email": info_data_row.info_email,
            "info_logo": info_data_row.info_logo,
            "info_icon": info_data_row.info_icon,
        }
        return return_info
    except Exception as e:
        db.rollback()
        logging.error(f"Exception: {e}")
        return {}