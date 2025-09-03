# ============================================= Start Noted JSON ===================================
# Author : Abdul Rohman Masrifan | masrifan26@gamil.com
# 1. Response return wajib JSON/dict supaya bisa diolah kembali di router
# ============================================= END Noted JSON ===================================
import os
from sqlalchemy.orm import Session, aliased
from core.modules.master.produk_barcode.model.produk_barcode_model import ProdukBarcodeModel
import barcode
from barcode.writer import ImageWriter

# Import json lainnya
from core.shared.json_helpers.json_global import json_data_timestamp
import logging
from core.config import UPLOAD_FOLDER

async def json_produk_barcode(db: Session, produk_barcode_data_row: ProdukBarcodeModel, timestamp_data: bool = False) -> dict:
    try:
        return_produk_barcode = {
            "productId"        : produk_barcode_data_row.productId,
            "productBarcode"   : produk_barcode_data_row.productBarcode,
            "productName"      : produk_barcode_data_row.productName,
            "image"            : produk_barcode_data_row.image,
            "sku"              : produk_barcode_data_row.sku,
            "plu"              : produk_barcode_data_row.plu,
            "categoryNameLvl0" : produk_barcode_data_row.categoryNameLvl0,
            "categoryNameLvl1" : produk_barcode_data_row.categoryNameLvl1,
            "categoryNameLvl2" : produk_barcode_data_row.categoryNameLvl2,
            "categoryIdLvl0"   : produk_barcode_data_row.categoryIdLvl0,
            "categoryIdLvl1"   : produk_barcode_data_row.categoryIdLvl1,
            "categoryIdLvl2"   : produk_barcode_data_row.categoryIdLvl2,
            "stock"            : produk_barcode_data_row.stock,
            "basePrice"        : produk_barcode_data_row.basePrice,
            "finalPrice"       : produk_barcode_data_row.finalPrice,
            "discountPercent"  : produk_barcode_data_row.discountPercent,
            "discountQty"      : produk_barcode_data_row.discountQty,
            "discountPrice"    : produk_barcode_data_row.discountPrice,
            "discountValue"    : produk_barcode_data_row.discountValue,
            "aktif"            : produk_barcode_data_row.aktif,
            "keterangan"       : produk_barcode_data_row.keterangan,
            # Tambahkan properti lain dari produk_barcode_data_row sesuai kebutuhan
        }

        # barcode_data = produk_barcode_data_row.productBarcode
        
        # if barcode_data:
        #     barcode_filename = f"{UPLOAD_FOLDER}/barcode/{barcode_data}"
        #     barcode_path = f"/static/barcode/{barcode_data}.png"  # Path untuk diakses di frontend
            
        #     # Jika barcode kurang dari 12 digit untuk EAN-13, gunakan Code128
        #     if len(barcode_data) == 12:
        #         ean = barcode.get_barcode_class('ean13')
        #         barcode_obj = ean(barcode_data, writer=ImageWriter())
        #     else:
        #         code128 = barcode.get_barcode_class('code128')
        #         barcode_obj = code128(barcode_data, writer=ImageWriter())

        #     # Simpan barcode sebagai gambar
        #     barcode_obj.save(barcode_filename)

        #     return_produk_barcode['productBarcodeImage'] = barcode_path  # Tambahkan barcode ke data produk

        return_produk_barcode['productBarcodeImage'] = None
        

        if timestamp_data:
            return_produk_barcode["timestamp_data"] = await json_data_timestamp(db=db, data_row=produk_barcode_data_row)

        return return_produk_barcode
    except Exception as e:
        db.rollback()
        logging.error(f"Exception: {e}")
        return {}