# ============================================= Start Noted JSON ===================================
# Author : PT. Dapur Perangkat Lunak Indonesia | KoffieSoft Group | https://www.koffiesoft.com/ | info@koffiesoft.com
# 1. Response return wajib JSON/dict supaya bisa diolah kembali di router
# ============================================= END Noted JSON ===================================
from sqlalchemy.orm import Session, aliased
from core.modules.satuan.model.satuan_model import SatuanModel

# Import json lainnya
import logging

async def json_satuan(db: Session, satuan_data_row: SatuanModel, timestamp_data: bool = False) -> dict:
    from core.shared.json_helpers.json_global import json_data_timestamp
    try:
        return_satuan = {
            "satuan_id"             : satuan_data_row.satuan_id,
            "satuan_kode"           : satuan_data_row.satuan_kode,
            "satuan_nama"           : satuan_data_row.satuan_nama,
            "satuan_aktif"          : satuan_data_row.satuan_aktif,
            "satuan_keterangan"     : satuan_data_row.satuan_keterangan,
            # Tambahkan properti lain dari satuan_data_row sesuai kebutuhan
        }
        if timestamp_data:
            return_satuan["timestamp_data"] = await json_data_timestamp(db=db, data_row=satuan_data_row)

        return return_satuan
    except Exception as e:
        db.rollback()
        logging.error(f"Exception: {e}")
        return {}