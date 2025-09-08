# ============================================= Start Noted JSON ===================================
# Author : PT. Dapur Perangkat Lunak Indonesia | KoffieSoft Group | https://www.koffiesoft.com/ | info@koffiesoft.com
# 1. Response return wajib JSON/dict supaya bisa diolah kembali di router
# ============================================= END Noted JSON ===================================
from sqlalchemy.orm import Session, aliased
from core.modules.customer.model.customer_model import CustomerModel
from sqlalchemy import text

# Import json lainnya
import logging

async def json_customer(
    db: Session, 
    customer_data_row: CustomerModel, 
    timestamp_data: bool = False
) -> dict:
    from core.shared.json_helpers.json_global import json_data_timestamp
    try:
        return_customer = {
            "cust_id"             : customer_data_row.cust_id,
            "cust_no"             : customer_data_row.cust_no,
            "cust_nama_lengkap"   : customer_data_row.cust_nama_lengkap,
            "cust_nama_panggilan" : customer_data_row.cust_nama_panggilan,
            "cust_kelamin"        : customer_data_row.cust_kelamin,
            "cust_alamat"         : customer_data_row.cust_alamat,
            "cust_hp"             : customer_data_row.cust_hp,
            "cust_aktif"          : customer_data_row.cust_aktif,
            "cust_keterangan"     : customer_data_row.cust_keterangan,
        }

        if timestamp_data:
            return_customer["timestamp_data"] = await json_data_timestamp(db=db, data_row=customer_data_row)

        return return_customer
    except Exception as e:
        db.rollback()
        logging.error(f"Exception: {e}")
        return {}
