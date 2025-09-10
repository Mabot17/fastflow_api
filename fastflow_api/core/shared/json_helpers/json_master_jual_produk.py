# ============================================= Start Noted JSON ===================================
# Author : PT. Dapur Perangkat Lunak Indonesia | KoffieSoft Group | https://www.koffiesoft.com/ | info@koffiesoft.com
# 1. Response return wajib JSON/dict supaya bisa diolah kembali di router
# ============================================= END Noted JSON ===================================
from sqlalchemy.orm import Session, aliased
from core.modules.master_jual_produk.model.master_jual_produk_model import MasterJualProdukModel

# Import json lainnya
import logging

async def json_master_jual_produk(
    db: Session, 
    master_jual_produk_data_row: MasterJualProdukModel, 
    timestamp_data: bool = False
) -> dict:
    from core.shared.json_helpers.json_global import json_data_timestamp, json_format_date
    from core.shared.json_helpers.json_customer import json_customer

    try:
        return_master_jual_produk = {
            "jproduk_id"         : master_jual_produk_data_row.jproduk_id,
            "jproduk_tanggal"    : json_format_date(master_jual_produk_data_row.jproduk_tanggal, '%Y-%m-%d'),
            "jproduk_nobukti"    : master_jual_produk_data_row.jproduk_nobukti,
            "jproduk_cust"       : master_jual_produk_data_row.jproduk_cust,
            "jproduk_diskon"     : master_jual_produk_data_row.jproduk_diskon,
            "jproduk_cara"       : master_jual_produk_data_row.jproduk_cara,
            "jproduk_stat_dok"   : master_jual_produk_data_row.jproduk_stat_dok,
            "jproduk_bayar"      : master_jual_produk_data_row.jproduk_bayar,
            "jproduk_totalbiaya" : master_jual_produk_data_row.jproduk_totalbiaya,
            "jproduk_keterangan" : master_jual_produk_data_row.jproduk_keterangan,
        }

        # opsional timestamp
        if timestamp_data:
            return_master_jual_produk["timestamp_data"] = await json_data_timestamp(
                db=db, 
                data_row=master_jual_produk_data_row
            )

        # relasi customer
        if master_jual_produk_data_row.jproduk_cust is not None and master_jual_produk_data_row.jproduk_cust > 0:
            cust_data = await json_customer(
                db=db, 
                customer_data_row=master_jual_produk_data_row.jproduk_cust_data
            )
            return_master_jual_produk["jproduk_cust_data"] = cust_data
        else:
            return_master_jual_produk["jproduk_cust_data"] = None

        return return_master_jual_produk
    except Exception as e:
        db.rollback()
        logging.error(f"Exception: {e}")
        return {}
