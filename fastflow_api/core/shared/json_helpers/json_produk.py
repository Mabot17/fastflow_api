# ============================================= Start Noted JSON ===================================
# Author : PT. Dapur Perangkat Lunak Indonesia | KoffieSoft Group | https://www.koffiesoft.com/ | info@koffiesoft.com
# 1. Response return wajib JSON/dict supaya bisa diolah kembali di router
# ============================================= END Noted JSON ===================================
from sqlalchemy.orm import Session, aliased
from core.modules.produk.model.produk_model import ProdukModel
from core.shared.check_data_model import check_produk

# Import json lainnya
import logging
    
async def json_produk(db: Session, produk_data_row: ProdukModel, timestamp_data: bool = False, produk_satuan_konversi_data: bool = False, produk_group_data: bool = False) -> dict:
    from core.shared.json_helpers.json_global import json_data_timestamp
    from core.shared.json_helpers.json_produk_group import json_produk_group
    from core.shared.json_helpers.json_satuan_konversi import json_satuan_konversi
    try:
        return_produk = {
            "produk_id"          : produk_data_row.produk_id,
            "produk_kode"        : produk_data_row.produk_kode,
            "produk_sku"         : produk_data_row.produk_sku,
            "produk_group"       : produk_data_row.produk_group,
            "produk_nama"        : produk_data_row.produk_nama,
            "produk_satuan"      : produk_data_row.produk_satuan,
            "produk_harga"       : produk_data_row.produk_harga,
            "produk_diskon"      : produk_data_row.produk_diskon,
            "produk_diskon_rp"   : produk_data_row.produk_diskon_rp,
            "produk_foto_path"   : produk_data_row.produk_foto_path,
            "produk_aktif"       : produk_data_row.produk_aktif,
            "produk_keterangan"  : produk_data_row.produk_keterangan,
        }

        # Menampilkan attribut json baru satuan
        if produk_data_row.produk_satuan is not None:
            return_produk["produk_satuan_nama"] = produk_data_row.produk_satuan_data.satuan_nama
        else:
            return_produk["produk_satuan_nama"] = None
        
        if timestamp_data:
            return_produk["timestamp_data"] = await json_data_timestamp(db=db, data_row=produk_data_row)

        if produk_satuan_konversi_data and produk_data_row.produk_satuan_konversi_data is not None:
            # Filter data untuk hanya menyertakan item dengan deleted_at = None
            produk_foto_detail_data = [
                row for row in produk_data_row.produk_satuan_konversi_data if row.deleted_at is None
            ]

            # Foreach async + tambahan field konversi_stok
            data_satuan_konversi = []
            for row in produk_foto_detail_data:
                # Ambil data asli dari fungsi JSON pembentuk
                row_data = await json_satuan_konversi(
                    db=db,
                    satuan_konversi_data_row=row,
                    konversi_satuan_data=True
                )
                data_satuan_konversi.append(row_data)

            return_produk["produk_satuan_konversi_data"] = data_satuan_konversi
        else:
            return_produk["produk_satuan_konversi_data"] = None

        if produk_group_data:
            if produk_data_row.produk_group is not None and produk_data_row.produk_group > 0:
                return_produk["produk_group_data"] = await json_produk_group(db=db, produk_group_data_row=produk_data_row.produk_group_data)
            else:
                return_produk["produk_group_data"] = None

        return return_produk
    except Exception as e:
        db.rollback()
        logging.error(f"Exception: {e}")
        return {}