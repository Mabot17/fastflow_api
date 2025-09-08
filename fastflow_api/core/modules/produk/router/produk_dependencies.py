# check_product.py

from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from fastapi import Request

from core.modules.produk.model.satuan_konversi_model import SatuanKonversiModel
from core.shared.check_data_model import (
    check_produk,
    check_produk_satuan_konversi
)

from core.utils.response_handle import (
    show_success_list,
    show_success,
    show_not_found,
    show_bad_response,
    show_bad_request,
    get_example_responses
)

# Fungsi pengecekan produk
async def check_and_return_produk(db: Session, produk_id: int, http_request: Request):
    check_produk_master = await check_produk(db, produk_id=produk_id)
    if not check_produk_master:
        result = await show_not_found(http_request=http_request, status_code=404, error=f"Produk dengan ID {produk_id} tidak ditemukan atau tidak aktif.")
        return JSONResponse(content=result, status_code=result['status']['code'])
    return None  # Jika produk ditemukan, return None untuk melanjutkan eksekusi

async def check_and_return_produk_satuan(db: Session, produk_id: int, satuan_id: int, http_request: Request, exclude_konversi_id: int = None):
    check_produk_satuan_master = await check_produk_satuan_konversi(db, produk_id=produk_id, satuan_id=satuan_id, exclude_konversi_id=exclude_konversi_id)
    if check_produk_satuan_master:
        result = await show_bad_request(http_request=http_request, status_code=400, error=f"Produk dengan ID {produk_id} dan Satuan ID {satuan_id} Sudah ada sebelumnya.")
        return JSONResponse(content=result, status_code=result['status']['code'])
    return None  # Jika produk ditemukan, return None untuk melanjutkan eksekusi

async def check_and_return_produk_satuan_sync(db: Session, produk_id: int, satuan_id: int, http_request: Request):
    """
    Validasi keberadaan satuan konversi berdasarkan ID produk dan satuan.
    Jika tidak ditemukan, kembalikan respons error 404.
    """
    satuan_konversi = db.query(SatuanKonversiModel).filter(
        SatuanKonversiModel.konversi_produk == produk_id,
        SatuanKonversiModel.konversi_satuan == satuan_id
    ).first()

    if not satuan_konversi:
        result = await show_not_found(
            http_request=http_request,
            status_code=404,
            error=f"Satuan dengan ID {satuan_id} tidak ditemukan pada produk ID {produk_id} atau tidak aktif."
        )
        return JSONResponse(content=result, status_code=result["status"]["code"])
    
    return None  # Valid, lanjutkan proses
