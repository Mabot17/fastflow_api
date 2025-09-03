# ============================================= Start Noted JSON ===================================
# Author : Abdul Rohman Masrifan | masrifan26@gamil.com
# 1. Response return wajib JSON/dict supaya bisa diolah kembali di router
# ============================================= END Noted JSON ===================================
from sqlalchemy.orm import Session, aliased
from core.modules.users.model.users_model import UsersModel

# Import modul json lainnya
from .json_global import json_data_timestamp
import logging

async def json_user(db: Session, user_data_row: UsersModel, timestamp_data: bool = False, data_group_detail: bool = False, user_karyawan_data: bool = False):
    try:
        return_users = {
            "user_id"         : user_data_row.user_id,
            "user_name"       : user_data_row.user_name,
            "user_aktif"      : user_data_row.user_aktif,
            "user_keterangan" : user_data_row.user_keterangan
        }

        if timestamp_data:
            return_users["timestamp_data"] = await json_data_timestamp(db=db, data_row=user_data_row)

        return return_users
    except Exception as e:
        db.rollback()
        logging.error(f"Exception: {e}")
        return {}