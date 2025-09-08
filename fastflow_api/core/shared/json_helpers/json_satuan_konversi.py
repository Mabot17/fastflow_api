# ============================================= Start Noted JSON ===================================
# Author : PT. Dapur Perangkat Lunak Indonesia | KoffieSoft Group | https://www.koffiesoft.com/ | info@koffiesoft.com
# 1. Response return wajib JSON/dict supaya bisa diolah kembali di router
# ============================================= END Noted JSON ===================================
from sqlalchemy.orm import Session, aliased
from core.modules.produk.model.satuan_konversi_model import SatuanKonversiModel
from sqlalchemy import and_, func, or_, text
from datetime import datetime
from core.utils.parsing import decrypt_query

# Import json lainnya
import logging

async def json_satuan_konversi(db: Session, satuan_konversi_data_row: SatuanKonversiModel, timestamp_data: bool = False, konversi_satuan_data: bool = False) -> dict:
    from core.shared.json_helpers.json_global import json_data_timestamp
    from core.shared.json_helpers.json_satuan import json_satuan
    try:
        return_satuan_konversi = {
            "konversi_id"         : satuan_konversi_data_row.konversi_id,
            "konversi_sku"        : satuan_konversi_data_row.konversi_sku,
            "konversi_produk"     : satuan_konversi_data_row.konversi_produk,
            "konversi_satuan"     : satuan_konversi_data_row.konversi_satuan,
            "konversi_nilai"      : float(satuan_konversi_data_row.konversi_nilai) if satuan_konversi_data_row.konversi_nilai is not None else 0.0,
            "konversi_harga"      : float(satuan_konversi_data_row.konversi_harga) if satuan_konversi_data_row.konversi_harga is not None else 0.0,
            "konversi_aktif"      : satuan_konversi_data_row.konversi_aktif,
            "konversi_default"    : satuan_konversi_data_row.konversi_default,
            "konversi_keterangan" : satuan_konversi_data_row.konversi_keterangan,
        }

        if timestamp_data:
            return_satuan_konversi["timestamp_data"] = await json_data_timestamp(db=db, data_row=satuan_konversi_data_row)

        if konversi_satuan_data:
            return_satuan_konversi["konversi_satuan_data"] = await json_satuan(db=db, satuan_data_row=satuan_konversi_data_row.konversi_satuan_data)

        return return_satuan_konversi
    except Exception as e:
        db.rollback()
        logging.error(f"Exception: {e}")
        return {}