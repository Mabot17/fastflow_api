# ============================================= Start Noted Router ===================================
# Author : PT. Dapur Perangkat Lunak Indonesia | KoffieSoft Group | https://www.koffiesoft.com/ | info@koffiesoft.com
# 1. @routerDetailMasterJualProduk.get("/daftar", response_model=DetailMasterJualProdukListSchema) >> routerDetailMasterJualProduk = abstrack class dari APIRouter. dipanggil di router/api_router.py
# 2. responseHandle = ResponseHandle() >> responseHandle = abstrack class standart dari core/utils/response_handle.py
# 3. async def get_daftar_detail_jual_produk() >> Nama function akan dijadikan title di main.py, misal get_daftar_detail_jual_produk
# 4. identity: UsersReqSchema = Depends(get_current_user),
#   - async def sample_function(
#       identity: UsersReqSchema = Depends(get_current_user) >> parameter `identity : ` Ini digunakan MENGGUNAKAN / TIDAK TOKEN saat akses api
# 5. Contoh rq ke file crud.py : get_daftar_detail_jual_produk && get_crud_daftar_detail_jual_produk dibedakan >> supaya memudahkan klik function
# 6. 'http_request: Request` >> menginisialisasikan scarlete.object untuk mengambil request awal dari http
# 7. request: DetailMasterJualProdukReqSchema = Depends(DetailMasterJualProdukReqSchema.as_form)
#       - request: DetailMasterJualProdukReqSchema = Depends(DetailMasterJualProdukReqSchema.as_form) -> type data form
#       - request: DetailMasterJualProdukReqSchema = application/json
# ============================================= END Noted Router ===================================
from fastapi import (
    APIRouter,
    Depends,
    status,
    Path,
    Query,
    Request,
    BackgroundTasks
)
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from database import get_db
from core.modules.master_jual_produk.crud.detail_jual_produk_crud import (
    get_crud_daftar_detail_jual_produk,
    select_detail_jual_produk_by_id,
    create_data_detail_jual_produk,
    update_data_detail_jual_produk,
    partial_update_data_detail_jual_produk,
    delete_data_detail_jual_produk
)
from core.modules.users.schema.users_schema import (
    UsersReqSchema,
)
from core.modules.master_jual_produk.schema.detail_jual_produk_schema import (
    DetailMasterJualProdukBaseDataSchema,
    DetailMasterJualProdukRequestListSchema,
    DetailMasterJualProdukListSchema,
    DetailMasterJualProdukReqSchema,
    DetailMasterJualProdukPatchSchema,
    DetailMasterJualProdukSingleSchema
)
from core.utils.oauth2 import get_current_user
from core.shared.check_data_model import (
    check_detail_jual_produk
)
from .master_jual_produk_dependencies import check_and_return_master_jual_produk
from core.utils.response_handle import (
    show_success_list,
    show_success,
    show_not_found,
    show_bad_response,
    show_bad_request,
    get_example_responses
)
import logging

# START CODE ROUTE Detail MasterJualProduk
routerDetailMasterJualProduk = APIRouter(tags=["Transaksi - Penjualan Produk - Detail Produk"], prefix="/detail_jual_produk")

example_responses = get_example_responses(status_codes=[401, 404, 405, 422, 500])

# ROUTE LIST & SEARCH DATA Detail MasterJualProduk
@routerDetailMasterJualProduk.get("/{jproduk_id}/detail_jual_produk", response_model=DetailMasterJualProdukListSchema, responses=example_responses)
async def get_all_detail_jual_produk(
    http_request: Request,
    jproduk_id: int = Path(..., description="ID dari API GET `/transaksi/master_jual_produk` (get_all_master_jual_produk) -> key `jproduk_id` "),
    request: DetailMasterJualProdukRequestListSchema = Depends(DetailMasterJualProdukRequestListSchema.as_form),
    identity: UsersReqSchema = Depends(get_current_user),
    db: Session = Depends(get_db),
):

    # Panggil pengecekan header
    check_data = await check_and_return_master_jual_produk(db=db, jproduk_id=jproduk_id, http_request=http_request)
    if check_data:
        return check_data  # Jika header tidak ditemukan, langsung return JSONResponse
    
    try:
        daftar = await get_crud_daftar_detail_jual_produk(db=db, jproduk_id=jproduk_id, request=request)
        # print(daftar)

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
        return JSONResponse(content=jsonable_encoder(result), status_code=result['status']['code'])
    except Exception as e:
        logging.error(f"Exception list_detail_jual_produk: {e}")
        result = show_bad_response(error=str(e), http_request=http_request)
        return JSONResponse(content=jsonable_encoder(result))

# ROUTE GET DATA Detail MasterJualProduk BY ID
@routerDetailMasterJualProduk.get("/{jproduk_id}/detail_jual_produk/{dproduk_id}", response_model=DetailMasterJualProdukSingleSchema, responses=example_responses)
async def get_detail_jual_produk(
    http_request: Request,
    timestamp_data: bool = Query(False, description="Jika true, JSON akan disertakan detail timestamp."),
    jproduk_id: int = Path(..., description="ID dari API GET `/transaksi/master_jual_produk` (get_all_master_jual_produk) -> key `jproduk_id` "),
    dproduk_id: int = Path(..., description="ID dari API GET `/detail_jual_produk` (get_all_detail_jual_produk) -> key `dproduk_id` "),
    db: Session = Depends(get_db),
    identity: UsersReqSchema = Depends(get_current_user),
):

    # Panggil pengecekan header
    check_data = await check_and_return_master_jual_produk(db=db, jproduk_id=jproduk_id, http_request=http_request)
    if check_data:
        return check_data  # Jika header tidak ditemukan, langsung return JSONResponse
    
    try:
        data_detail_jual_produk = await select_detail_jual_produk_by_id(db, jproduk_id=jproduk_id, dproduk_id=dproduk_id, timestamp_data=timestamp_data)
        if not data_detail_jual_produk:
            result = await show_not_found(http_request=http_request, status_code=404, error=f"Point Of Sales ID {jproduk_id} dengan Detail Point Of Sales ID {dproduk_id} tidak ditemukan atau tidak aktif.")
        else:
            result = await show_success(data=data_detail_jual_produk, http_request=http_request, status_code=status.HTTP_200_OK)

        # Return result['status']['code'] akan dikembalikan sesuai yang dikirim diatas,
        return JSONResponse(content=jsonable_encoder(result), status_code=result['status']['code'])
    except Exception as e:
        logging.error(f"Exception single_list_detail_jual_produk: {e}")
        result = show_bad_response(error=str(e), http_request=http_request)
        return JSONResponse(content=jsonable_encoder(result))

# ROUTE CREATE DATA Detail MasterJualProduk
@routerDetailMasterJualProduk.post("/{jproduk_id}/detail_jual_produk", response_model=DetailMasterJualProdukSingleSchema, responses=example_responses)
async def create_detail_jual_produk(
    http_request: Request,
    bt: BackgroundTasks,
    request: DetailMasterJualProdukReqSchema,
    jproduk_id: int = Path(..., description="ID dari API GET `/transaksi/master_jual_produk` (get_all_master_jual_produk) -> key `jproduk_id` "),
    db: Session = Depends(get_db),
    identity: UsersReqSchema = Depends(get_current_user),
):
    
    """
        **Catatan Atribut:** 

        - `dproduk_produk`: ID dari API GET `/master/produk` (get_all_produk) -> key `produk_id` \n
        - `dproduk_satuan`: ID dari API GET `/master/produk/{produk_id}/satuan_konversi` (get_all_satuan_konversi) -> key `konversi_satuan` \n
        - `dproduk_harga`: dari API GET `/master/produk/{produk_id}/satuan_konversi` (get_all_satuan_konversi) -> key `konversi_harga` \n
        - `dproduk_diskon`: diskon persen \n
        - `dproduk_diskon_rp`: diskon rupiah \n\n

        **Untuk attribut `dproduk_diskon` dan `dproduk_diskon_rp`, hanya boleh diisi salah satu saja**
    """
        
    # Panggil pengecekan header
    check_data = await check_and_return_master_jual_produk(db=db, jproduk_id=jproduk_id, http_request=http_request)
    if check_data:
        return check_data  # Jika header tidak ditemukan, langsung return JSONResponse
        
    try:
        new_detail_jual_produk = await create_data_detail_jual_produk(db=db, jproduk_id=jproduk_id, detail_jual_produk_data_create=request, identity=identity)
        if new_detail_jual_produk:
            result = await show_success(data=new_detail_jual_produk, http_request=http_request, code_message='createTrue', status_code=status.HTTP_201_CREATED)
        else:
            result = await show_success(http_request=http_request, code_message='createFalse', status_code=status.HTTP_422_UNPROCESSABLE_ENTITY)
            
        return JSONResponse(content=jsonable_encoder(result), status_code=result['status']['code'])
    except Exception as e:
        logging.error(f"Exception create_detail_jual_produk: {e}")
        result = show_bad_response(error=str(e), http_request=http_request)
        return JSONResponse(content=jsonable_encoder(result), status_code=result['status']['code'])

# ROUTE UPDATE DATA Detail MasterJualProduk
@routerDetailMasterJualProduk.put("/{jproduk_id}/detail_jual_produk/{dproduk_id}", response_model=DetailMasterJualProdukSingleSchema, responses=example_responses)
async def update_detail_jual_produk(
    http_request: Request,
    request: DetailMasterJualProdukReqSchema,
    jproduk_id: int = Path(..., description="ID dari API GET `/transaksi/master_jual_produk` (get_all_master_jual_produk) -> key `jproduk_id` "),
    dproduk_id: int = Path(..., description="ID dari API GET `/detail_jual_produk` (get_all_detail_jual_produk) -> key `dproduk_id` "),
    db: Session = Depends(get_db),
    identity: UsersReqSchema = Depends(get_current_user),
):
    
    """
        **Catatan Atribut:** 

        - `dproduk_produk`: ID dari API GET `/master/produk` (get_all_produk) -> key `produk_id` \n
        - `dproduk_satuan`: ID dari API GET `/master/produk/{produk_id}/satuan_konversi` (get_all_satuan_konversi) -> key `konversi_satuan` \n
        - `dproduk_harga`: dari API GET `/master/produk/{produk_id}/satuan_konversi` (get_all_satuan_konversi) -> key `konversi_harga` \n
        - `dproduk_diskon`: diskon persen \n
        - `dproduk_diskon_rp`: diskon rupiah \n\n

        **Untuk attribut `dproduk_diskon` dan `dproduk_diskon_rp`, hanya boleh diisi salah satu saja**
    """

    # Panggil pengecekan header
    check_data = await check_and_return_master_jual_produk(db=db, jproduk_id=jproduk_id, http_request=http_request)
    if check_data:
        return check_data  # Jika header tidak ditemukan, langsung return JSONResponse
            
    try:
        check_data_detail_jual_produk = await check_detail_jual_produk(db, dproduk_id=dproduk_id, jproduk_id=jproduk_id)
        if not check_data_detail_jual_produk:
            result = await show_not_found(http_request=http_request, status_code=404, error=f"Point Of Sales ID {jproduk_id} dengan Detail Point Of Sales ID {dproduk_id} tidak ditemukan atau tidak aktif.")
        else:
            data_detail_jual_produk = await update_data_detail_jual_produk(db=db, jproduk_id=jproduk_id, dproduk_id=dproduk_id, detail_jual_produk_data_update=request, identity=identity)
            result = await show_success(data=data_detail_jual_produk, http_request=http_request, status_code=status.HTTP_200_OK)

        # Return result['status']['code'] akan dikembalikan sesuai yang dikirim diatas,
        return JSONResponse(content=jsonable_encoder(result), status_code=result['status']['code'])
    except Exception as e:
        logging.error(f"Exception update_detail_jual_produk: {e}")
        result = show_bad_response(error=str(e), http_request=http_request)
        return JSONResponse(content=jsonable_encoder(result))
    
# ROUTE UPDATE PATCH DATA Detail MasterJualProduk
@routerDetailMasterJualProduk.patch("/{jproduk_id}/detail_jual_produk/{dproduk_id}", response_model=DetailMasterJualProdukSingleSchema, responses=example_responses)
async def partial_update_detail_jual_produk(
    http_request: Request,
    request: DetailMasterJualProdukPatchSchema,
    jproduk_id: int = Path(..., description="ID dari API GET `/transaksi/master_jual_produk` (get_all_master_jual_produk) -> key `jproduk_id` "),
    dproduk_id: int = Path(..., description="ID dari API GET `/detail_jual_produk` (get_all_detail_jual_produk) -> key `dproduk_id` "),
    db: Session = Depends(get_db),
    identity: UsersReqSchema = Depends(get_current_user),
):
    
    """
        **Catatan Atribut:** 

        - `dproduk_produk`: ID dari API GET `/master/produk` (get_all_produk) -> key `produk_id` \n
        - `dproduk_satuan`: ID dari API GET `/master/produk/{produk_id}/satuan_konversi` (get_all_satuan_konversi) -> key `konversi_satuan` \n
        - `dproduk_harga`: dari API GET `/master/produk/{produk_id}/satuan_konversi` (get_all_satuan_konversi) -> key `konversi_harga` \n
        - `dproduk_diskon`: diskon persen \n
        - `dproduk_diskon_rp`: diskon rupiah \n\n

        **Untuk attribut `dproduk_diskon` dan `dproduk_diskon_rp`, hanya boleh diisi salah satu saja**
    """

    # Panggil pengecekan header
    check_data = await check_and_return_master_jual_produk(db=db, jproduk_id=jproduk_id, http_request=http_request)
    if check_data:
        return check_data  # Jika header tidak ditemukan, langsung return JSONResponse
            
    try:
        check_data_detail_jual_produk = await check_detail_jual_produk(db, dproduk_id=dproduk_id, jproduk_id=jproduk_id)
        if not check_data_detail_jual_produk:
            result = await show_not_found(http_request=http_request, status_code=404, error=f"Point Of Sales ID {jproduk_id} dengan Detail Point Of Sales ID {dproduk_id} tidak ditemukan atau tidak aktif.")
        else:
            data_detail_jual_produk = await partial_update_data_detail_jual_produk(db=db, jproduk_id=jproduk_id, dproduk_id=dproduk_id, detail_jual_produk_data_update=request.dict(exclude_unset=True), identity=identity)
            result = await show_success(data=data_detail_jual_produk, http_request=http_request, status_code=status.HTTP_200_OK)

        # Return result['status']['code'] akan dikembalikan sesuai yang dikirim diatas,
        return JSONResponse(content=jsonable_encoder(result), status_code=result['status']['code'])
    except Exception as e:
        logging.error(f"Exception update_patch_detail_jual_produk: {e}")
        result = show_bad_response(error=str(e), http_request=http_request)
        return JSONResponse(content=jsonable_encoder(result))

# ROUTE DELETE DATA Detail MasterJualProduk
@routerDetailMasterJualProduk.delete("/{jproduk_id}/detail_jual_produk/{dproduk_id}", response_model=DetailMasterJualProdukSingleSchema, responses=example_responses)
async def delete_detail_jual_produk(
    http_request: Request,
    jproduk_id: int = Path(..., description="ID dari API GET `/transaksi/master_jual_produk` (get_all_master_jual_produk) -> key `jproduk_id` "),
    dproduk_id: int = Path(..., description="ID dari API GET `/detail_jual_produk` (get_all_detail_jual_produk) -> key `dproduk_id` "),
    db: Session = Depends(get_db),
    identity: UsersReqSchema = Depends(get_current_user),
):

    # Panggil pengecekan header
    check_data = await check_and_return_master_jual_produk(db=db, jproduk_id=jproduk_id, http_request=http_request)
    if check_data:
        return check_data  # Jika header tidak ditemukan, langsung return JSONResponse
    
    try:
        check_data_detail_jual_produk = await check_detail_jual_produk(db, dproduk_id=dproduk_id, jproduk_id=jproduk_id)
        if not check_data_detail_jual_produk:
            result = await show_not_found(http_request=http_request, status_code=404, error=f"Point Of Sales ID {jproduk_id} dengan Detail Point Of Sales ID {dproduk_id} tidak ditemukan atau tidak aktif.")
        else:
            deleted_data_detail_jual_produk = await delete_data_detail_jual_produk(db=db, jproduk_id=jproduk_id, dproduk_id=dproduk_id, identity=identity)
            result = await show_success(data=deleted_data_detail_jual_produk, http_request=http_request, status_code=status.HTTP_200_OK)

        # Return result['status']['code'] akan dikembalikan sesuai yang dikirim diatas,
        return JSONResponse(content=jsonable_encoder(result), status_code=result['status']['code'])
    except Exception as e:
        logging.error(f"Exception delete_detail_jual_produk: {e}")
        result = show_bad_response(error=str(e), http_request=http_request)
        return JSONResponse(content=jsonable_encoder(result))
    
# END CODE ROUTE Detail MasterJualProduk