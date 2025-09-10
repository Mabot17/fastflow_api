# ============================================= Start Noted JSON ===================================
# Author : PT. Dapur Perangkat Lunak Indonesia | KoffieSoft Group | https://www.koffiesoft.com/ | info@koffiesoft.com
# 1. Response return wajib JSON/dict supaya bisa diolah kembali di router
# ============================================= END Noted JSON ===================================
from sqlalchemy.orm import Session, aliased
from core.modules.master_jual_produk.model.detail_jual_produk_model import DetailJualProdukModel

# Import json lainnya
import logging

async def json_detail_jual_produk(db: Session, detail_jual_produk_data_row: DetailJualProdukModel, timestamp_data: bool = False, dproduk_produk_data: bool = False, dproduk_satuan_data: bool = False) -> dict:
    from core.shared.json_helpers.json_global import json_data_timestamp
    from core.shared.json_helpers.json_produk import json_produk
    from core.shared.json_helpers.json_satuan import json_satuan

    try:

        return_detail_jual_produk = {
            "dproduk_id"        : detail_jual_produk_data_row.dproduk_id,
            "dproduk_master"    : detail_jual_produk_data_row.dproduk_master,
            "dproduk_produk"    : detail_jual_produk_data_row.dproduk_produk,
            "dproduk_satuan"    : detail_jual_produk_data_row.dproduk_satuan,
            "dproduk_jumlah"    : float(detail_jual_produk_data_row.dproduk_jumlah) if detail_jual_produk_data_row.dproduk_jumlah is not None else 0.0,
            "dproduk_harga"     : float(detail_jual_produk_data_row.dproduk_harga) if detail_jual_produk_data_row.dproduk_harga is not None else 0.0,
            "dproduk_diskon"    : float(detail_jual_produk_data_row.dproduk_diskon) if detail_jual_produk_data_row.dproduk_diskon is not None else 0.0,
            "dproduk_diskon_rp" : float(detail_jual_produk_data_row.dproduk_diskon_rp) if detail_jual_produk_data_row.dproduk_diskon_rp is not None else 0.0,
            # Tambahkan properti lain dari detail_jual_produk_data_row sesuai kebutuhan
        }
        if timestamp_data:
            return_detail_jual_produk["timestamp_data"] = await json_data_timestamp(db=db, data_row=detail_jual_produk_data_row)

        if dproduk_produk_data:
            return_detail_jual_produk["dproduk_produk_data"] = await json_produk(db=db, produk_data_row=detail_jual_produk_data_row.dproduk_produk_data)

        if dproduk_satuan_data:
            return_detail_jual_produk["dproduk_satuan_data"] = await json_satuan(db=db, satuan_data_row=detail_jual_produk_data_row.dproduk_satuan_data)

        return return_detail_jual_produk
    except Exception as e:
        db.rollback()
        logging.error(f"Exception: {e}")
        return {}