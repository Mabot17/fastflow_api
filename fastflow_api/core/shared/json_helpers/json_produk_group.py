# ============================================= Start Noted JSON ===================================
# Author : PT. Dapur Perangkat Lunak Indonesia | KoffieSoft Group | https://www.koffiesoft.com/ | info@koffiesoft.com
# 1. Response return wajib JSON/dict supaya bisa diolah kembali di router
# ============================================= END Noted JSON ===================================
from sqlalchemy.orm import Session, aliased
from core.modules.produk_group.model.produk_group_model import ProdukGroupModel

# Import json lainnya
import logging

async def json_produk_group(db: Session, produk_group_data_row: ProdukGroupModel, timestamp_data: bool = False) -> dict:
    from core.shared.json_helpers.json_global import json_data_timestamp
    try:
        return_produk_group = {
            "group_id"             : produk_group_data_row.group_id,
            "group_kode"           : produk_group_data_row.group_kode,
            "group_nama"           : produk_group_data_row.group_nama,
            "group_aktif"          : produk_group_data_row.group_aktif,
            "group_keterangan"     : produk_group_data_row.group_keterangan,
            # Tambahkan properti lain dari produk_group_data_row sesuai kebutuhan
        }
        if timestamp_data:
            return_produk_group["timestamp_data"] = await json_data_timestamp(db=db, data_row=produk_group_data_row)

        return return_produk_group
    except Exception as e:
        db.rollback()
        logging.error(f"Exception: {e}")
        return {}