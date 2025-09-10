# ============================================= Start Noted Router ===================================
# Author : PT. Dapur Perangkat Lunak Indonesia | KoffieSoft Group | https://www.koffiesoft.com/ | info@koffiesoft.com
# 1. @routerMasterJualProduk.get("/daftar", response_model=MasterJualProdukListSchema) >> routerMasterJualProduk = abstrack class dari APIRouter. dipanggil di router/api_router.py
# 2. responseHandle = ResponseHandle() >> responseHandle = abstrack class standart dari core/utils/response_handle.py
# 3. async def get_daftar_master_jual_produk() >> Nama function akan dijadikan title di main.py, misal get_daftar_master_jual_produk
# 4. identity: UsersReqSchema = Depends(get_current_user),
#   - async def sample_function(
#       identity: UsersReqSchema = Depends(get_current_user) >> parameter `identity : ` Ini digunakan MENGGUNAKAN / TIDAK TOKEN saat akses api
# 5. Contoh rq ke file crud.py : get_daftar_master_jual_produk && get_crud_daftar_master_jual_produk dibedakan >> supaya memudahkan klik function
# 6. 'http_request: Request` >> menginisialisasikan scarlete.object untuk mengambil request awal dari http
# 7. request: MasterJualProdukReqSchema = Depends(MasterJualProdukReqSchema.as_form)
#       - request: MasterJualProdukReqSchema = Depends(MasterJualProdukReqSchema.as_form) -> type data form
#       - request: MasterJualProdukReqSchema = application/json
# ============================================= END Noted Router ===================================
import os
from core import config
from fastapi import (
    APIRouter,
    Depends,
    status,
    Path,
    Query,
    Request,
    BackgroundTasks
)
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from database import get_db
from core.modules.master_jual_produk.crud.master_jual_produk_crud import (
    get_crud_daftar_master_jual_produk,
    select_master_jual_produk_by_id,
    create_data_master_jual_produk,
    update_data_master_jual_produk,
    partial_update_data_master_jual_produk,
    delete_data_master_jual_produk,
)
from core.modules.users.schema.users_schema import (
    UsersReqSchema,
)
from core.modules.master_jual_produk.schema.master_jual_produk_schema import (
    MasterJualProdukBaseDataSchema,
    MasterJualProdukRequestListSchema,
    MasterJualProdukListSchema,
    MasterJualProdukReqSchema,
    MasterJualProdukPutSchema,
    MasterJualProdukPatchSchema,
    MasterJualProdukSingleSchema,
)
from core.utils.oauth2 import get_current_user
from core.shared.check_data_model import (
    check_master_jual_produk,
)
from core.utils.response_handle import (
    show_success_list,
    show_success,
    show_not_found,
    show_bad_response,
    show_bad_request,
    get_example_responses
)
import logging

# START CODE ROUTE Point Of Sales
routerMasterJualProduk = APIRouter(tags=["Transaksi - Penjualan Produk"], prefix="/master_jual_produk")

example_responses = get_example_responses(status_codes=[401, 404, 405, 422, 500])

# ROUTE LIST & SEARCH DATA Point Of Sales
@routerMasterJualProduk.get("", response_model=MasterJualProdukListSchema, responses=example_responses)
async def get_all_master_jual_produk(
    http_request: Request,
    request: MasterJualProdukRequestListSchema = Depends(MasterJualProdukRequestListSchema.as_form),
    identity: UsersReqSchema = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    try:
        daftar = await get_crud_daftar_master_jual_produk(db=db, request=request)

        if(daftar.get('total_data')):
            result = await show_success_list(
                http_request=http_request,
                data=daftar.get('data'),
                total_data=daftar.get('total_data'),
                page=request.page,
                results_per_page=request.results_per_page,
                is_paging=True,
            )
        else:
            result = await show_not_found(http_request=http_request, status_code=404)

        # Return result['status']['code'] akan dikembalikan sesuai yang dikirim diatas,
        return JSONResponse(content=result, status_code=result['status']['code'])
    except Exception as e:
        logging.error(f"Exception list_master_jual_produk: {e}")
        result = show_bad_response(error=str(e), http_request=http_request)
        return JSONResponse(content=result)

# ROUTE GET DATA Point Of Sales BY ID
@routerMasterJualProduk.get("/{jproduk_id}", response_model=MasterJualProdukSingleSchema, responses=example_responses)
async def get_master_jual_produk(
    http_request: Request,
    timestamp_data: bool = Query(False, description="Jika true, JSON akan disertakan detail timestamp."),
    jproduk_id: int = Path(..., description="ID dari API GET `/transaksi/master_jual_produk` (get_all_master_jual_produk) -> key `jproduk_id` "),
    db: Session = Depends(get_db),
    identity: UsersReqSchema = Depends(get_current_user),
):
    try:
        data_master_jual_produk = await select_master_jual_produk_by_id(db, jproduk_id=jproduk_id, timestamp_data=timestamp_data)
        if not data_master_jual_produk:
            result = await show_not_found(http_request=http_request, status_code=404)
        else:
            result = await show_success(data=data_master_jual_produk, http_request=http_request, status_code=status.HTTP_200_OK)

        # Return result['status']['code'] akan dikembalikan sesuai yang dikirim diatas,
        return JSONResponse(content=result, status_code=result['status']['code'])
    except Exception as e:
        logging.error(f"Exception single_list_master_jual_produk: {e}")
        result = show_bad_response(error=str(e), http_request=http_request)
        return JSONResponse(content=result)

# ROUTE CREATE DATA Point Of Sales
@routerMasterJualProduk.post("", response_model=MasterJualProdukSingleSchema, responses=example_responses)
async def create_master_jual_produk(
    http_request: Request,
    bt: BackgroundTasks,
    request: MasterJualProdukReqSchema,
    db: Session = Depends(get_db),
    identity: UsersReqSchema = Depends(get_current_user),
):
    
    """
        **Catatan:** 

        - `jproduk_tanggal`    : [Date] `Y-m-d` contoh penggunaan `2025-01-21` \n
        - `jproduk_cust`       : [Int] ID dari API GET `/master/customer` (get_all_customer) -> key `cust_id` \n
        - `jproduk_diskon`     : [Float] Potongan harga (dalam angka nominal, bukan persen) \n
        - `jproduk_cara`       : [Str] Metode/cara pembayaran (misal: 'Tunai', 'Kredit', 'Transfer') \n
        - `jproduk_keterangan` : [Str] Text bebas untuk catatan tambahan \n
        - `jproduk_stat_dok`   : [ENUM] pilihan `Terbuka`, `Tertutup`, `Batal`, `Tunggu`, `Sementara` \n
        - `jproduk_bayar`      : [Float] Jumlah total item dari detail produk \n
        - `jproduk_totalbiaya` : [Float] Jumlah nilai rupiah dari detail produk (sebelum/dikurangi diskon) \n
    """
        
    try:
        new_master_jual_produk = await create_data_master_jual_produk(db=db, master_jual_produk_data_create=request, identity=identity)
        if new_master_jual_produk:
            result = await show_success(data=new_master_jual_produk, http_request=http_request, code_message='createTrue', status_code=status.HTTP_201_CREATED)
        else:
            result = await show_success(http_request=http_request, code_message='createFalse', status_code=status.HTTP_422_UNPROCESSABLE_ENTITY)
            
        return JSONResponse(content=result, status_code=result['status']['code'])
    except Exception as e:
        logging.error(f"Exception create_master_jual_produk: {e}")
        result = show_bad_response(error=str(e), http_request=http_request)
        return JSONResponse(content=result, status_code=result['status']['code'])

# ROUTE UPDATE DATA Point Of Sales
@routerMasterJualProduk.put("/{jproduk_id}", response_model=MasterJualProdukSingleSchema, responses=example_responses)
async def update_master_jual_produk(
    http_request: Request,
    request: MasterJualProdukPutSchema,
    jproduk_id: int = Path(..., description="ID dari API GET `/transaksi/master_jual_produk` (get_all_master_jual_produk) -> key `jproduk_id` "),
    db: Session = Depends(get_db),
    identity: UsersReqSchema = Depends(get_current_user),
):
    
    """
        **Catatan:** 

        - `jproduk_tanggal`    : [Date] `Y-m-d` contoh penggunaan `2025-01-21` \n
        - `jproduk_cust`       : [Int] ID dari API GET `/master/customer` (get_all_customer) -> key `cust_id` \n
        - `jproduk_diskon`     : [Float] Potongan harga (dalam angka nominal, bukan persen) \n
        - `jproduk_cara`       : [Str] Metode/cara pembayaran (misal: 'Tunai', 'Kredit', 'Transfer') \n
        - `jproduk_keterangan` : [Str] Text bebas untuk catatan tambahan \n
        - `jproduk_stat_dok`   : [ENUM] pilihan `Terbuka`, `Tertutup`, `Batal`, `Tunggu`, `Sementara` \n
        - `jproduk_bayar`      : [Float] Jumlah total item dari detail produk \n
        - `jproduk_totalbiaya` : [Float] Jumlah nilai rupiah dari detail produk (sebelum/dikurangi diskon) \n
    """
        
    try:
        check_data_master_jual_produk = await check_master_jual_produk(db, jproduk_id=jproduk_id)
        if not check_data_master_jual_produk:
            result = await show_not_found(http_request=http_request, status_code=404)
        else:
            data_master_jual_produk = await update_data_master_jual_produk(db=db, jproduk_id=jproduk_id, master_jual_produk_data_update=request, identity=identity)
            result = await show_success(data=data_master_jual_produk, http_request=http_request, status_code=status.HTTP_200_OK)

        # Return result['status']['code'] akan dikembalikan sesuai yang dikirim diatas,
        return JSONResponse(content=result, status_code=result['status']['code'])
    except Exception as e:
        logging.error(f"Exception update_master_jual_produk: {e}")
        result = show_bad_response(error=str(e), http_request=http_request)
        return JSONResponse(content=result)
    
# ROUTE UPDATE PATCH DATA Point Of Sales
@routerMasterJualProduk.patch("/{jproduk_id}", response_model=MasterJualProdukSingleSchema, responses=example_responses)
async def partial_update_master_jual_produk(
    http_request: Request,
    request: MasterJualProdukPatchSchema,
    jproduk_id: int = Path(..., description="ID dari API GET `/transaksi/master_jual_produk` (get_all_master_jual_produk) -> key `jproduk_id` "),
    db: Session = Depends(get_db),
    identity: UsersReqSchema = Depends(get_current_user),
):
    
    """
        **Catatan:** 

        - `jproduk_tanggal`    : [Date] `Y-m-d` contoh penggunaan `2025-01-21` \n
        - `jproduk_cust`       : [Int] ID dari API GET `/master/customer` (get_all_customer) -> key `cust_id` \n
        - `jproduk_diskon`     : [Float] Potongan harga (dalam angka nominal, bukan persen) \n
        - `jproduk_cara`       : [Str] Metode/cara pembayaran (misal: 'Tunai', 'Kredit', 'Transfer') \n
        - `jproduk_keterangan` : [Str] Text bebas untuk catatan tambahan \n
        - `jproduk_stat_dok`   : [ENUM] pilihan `Terbuka`, `Tertutup`, `Batal`, `Tunggu`, `Sementara` \n
        - `jproduk_bayar`      : [Float] Jumlah total item dari detail produk \n
        - `jproduk_totalbiaya` : [Float] Jumlah nilai rupiah dari detail produk (sebelum/dikurangi diskon) \n
    """
        
    try:
        check_data_master_jual_produk = await check_master_jual_produk(db, jproduk_id=jproduk_id)
        if not check_data_master_jual_produk:
            result = await show_not_found(http_request=http_request, status_code=404)
        else:
            data_master_jual_produk = await partial_update_data_master_jual_produk(db=db, jproduk_id=jproduk_id, master_jual_produk_data_update=request.dict(exclude_unset=True), identity=identity)
            result = await show_success(data=data_master_jual_produk, http_request=http_request, status_code=status.HTTP_200_OK)

        # Return result['status']['code'] akan dikembalikan sesuai yang dikirim diatas,
        return JSONResponse(content=result, status_code=result['status']['code'])
    except Exception as e:
        logging.error(f"Exception update_patch_master_jual_produk: {e}")
        result = show_bad_response(error=str(e), http_request=http_request)
        return JSONResponse(content=result)

# ROUTE DELETE DATA Point Of Sales
@routerMasterJualProduk.delete("/{jproduk_id}", response_model=MasterJualProdukSingleSchema, responses=example_responses)
async def delete_master_jual_produk(
    http_request: Request,
    jproduk_id: int = Path(..., description="ID dari API GET `/transaksi/master_jual_produk` (get_all_master_jual_produk) -> key `jproduk_id` "),
    db: Session = Depends(get_db),
    identity: UsersReqSchema = Depends(get_current_user),
):
    try:
        check_data_master_jual_produk = await check_master_jual_produk(db, jproduk_id=jproduk_id)
        if not check_data_master_jual_produk:
            result = await show_not_found(http_request=http_request, status_code=404)
        else:
            deleted_data_master_jual_produk = await delete_data_master_jual_produk(db=db, jproduk_id=jproduk_id, identity=identity)
            result = await show_success(data=deleted_data_master_jual_produk, http_request=http_request, status_code=status.HTTP_200_OK)

        # Return result['status']['code'] akan dikembalikan sesuai yang dikirim diatas,
        return JSONResponse(content=result, status_code=result['status']['code'])
    except Exception as e:
        logging.error(f"Exception delete_master_jual_produk: {e}")
        result = show_bad_response(error=str(e), http_request=http_request)
        return JSONResponse(content=result)
# END CODE ROUTE Point Of Sales