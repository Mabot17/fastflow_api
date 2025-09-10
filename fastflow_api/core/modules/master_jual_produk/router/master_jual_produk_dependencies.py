# check_product.py

from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from fastapi import Request

from core.shared.check_data_model import (
    check_master_jual_produk
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
async def check_and_return_master_jual_produk(db: Session, jproduk_id: int, http_request: Request):
    check_master = await check_master_jual_produk(db, jproduk_id=jproduk_id)
    if not check_master:
        result = await show_not_found(http_request=http_request, status_code=404, error=f"Master Jual Produk dengan ID {jproduk_id} tidak ditemukan atau tidak aktif.")
        return JSONResponse(content=result, status_code=result['status']['code'])
    return None  # Jika produk ditemukan, return None untuk melanjutkan eksekusi
