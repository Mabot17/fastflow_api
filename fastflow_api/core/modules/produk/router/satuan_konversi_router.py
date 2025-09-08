# ============================================= Start Noted Router ===================================
# Author : PT. Dapur Perangkat Lunak Indonesia | KoffieSoft Group | https://www.koffiesoft.com/ | info@koffiesoft.com
# 1. @routerSatuanKonversi.get("/daftar", response_model=SatuanKonversiListSchema) >> routerSatuanKonversi = abstrack class dari APIRouter. dipanggil di router/api_router.py
# 2. responseHandle = ResponseHandle() >> responseHandle = abstrack class standart dari core/utils/response_handle.py
# 3. async def get_daftar_satuan_konversi() >> Nama function akan dijadikan title di main.py, misal get_daftar_satuan_konversi
# 4. identity: UsersReqSchema = Depends(get_current_user),
#   - async def sample_function(
#       identity: UsersReqSchema = Depends(get_current_user) >> parameter `identity : ` Ini digunakan MENGGUNAKAN / TIDAK TOKEN saat akses api
# 5. Contoh rq ke file crud.py : get_daftar_satuan_konversi && get_crud_daftar_satuan_konversi dibedakan >> supaya memudahkan klik function
# 6. 'http_request: Request` >> menginisialisasikan scarlete.object untuk mengambil request awal dari http
# 7. request: SatuanKonversiReqSchema = Depends(SatuanKonversiReqSchema.as_form)
#       - request: SatuanKonversiReqSchema = Depends(SatuanKonversiReqSchema.as_form) -> type data form
#       - request: SatuanKonversiReqSchema = application/json
# ============================================= END Noted Router ===================================
from fastapi import (
    APIRouter,
    Depends,
    status,
    Path,
    Query,
    Request,
    BackgroundTasks,
    HTTPException
)
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from database import get_db
from core.modules.produk.crud.satuan_konversi_crud import (
    get_crud_daftar_satuan_konversi,
    select_satuan_konversi_by_id,
    create_data_satuan_konversi,
    update_data_satuan_konversi,
    partial_update_data_satuan_konversi,
    delete_data_satuan_konversi
)
from core.modules.users.schema.users_schema import (
    UsersReqSchema,
)
from core.modules.produk.schema.satuan_konversi_schema import (
    SatuanKonversiBaseDataSchema,
    SatuanKonversiRequestListSchema,
    SatuanKonversiListSchema,
    SatuanKonversiReqSchema,
    SatuanKonversiPatchSchema,
    SatuanKonversiSingleSchema
)
from core.utils.oauth2 import get_current_user
from core.shared.check_data_model import (
    check_satuan_konversi
)
from .produk_dependencies import check_and_return_produk, check_and_return_produk_satuan
from core.utils.response_handle import (
    show_success_list,
    show_success,
    show_not_found,
    show_bad_response,
    show_bad_request,
    get_example_responses
)
import logging

# START CODE ROUTE Satuan Konversi
routerSatuanKonversi = APIRouter(tags=["Master - Produk - Detail Satuan Konversi"], prefix="/produk")

example_responses = get_example_responses(status_codes=[401, 404, 405, 422, 500])

# ROUTE LIST & SEARCH DATA Satuan Konversi
@routerSatuanKonversi.get("/{produk_id}/satuan_konversi", response_model=SatuanKonversiListSchema, responses=example_responses)
async def get_all_satuan_konversi(
    http_request: Request,
    produk_id: int = Path(..., description="ID dari API GET `/master/produk` (get_all_produk) -> key `produk_id` "),
    request: SatuanKonversiRequestListSchema = Depends(SatuanKonversiRequestListSchema.as_form),
    identity: UsersReqSchema = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    
    # Panggil pengecekan produk
    check_data = await check_and_return_produk(db, produk_id, http_request)
    if check_data:
        return check_data  # Jika produk tidak ditemukan, langsung return JSONResponse

    try:
        daftar = await get_crud_daftar_satuan_konversi(db=db, produk_id=produk_id, request=request)
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
        return JSONResponse(content=result, status_code=result['status']['code'])
    except Exception as e:
        logging.error(f"Exception list_satuan_konversi: {e}")
        result = show_bad_response(error=str(e), http_request=http_request)
        return JSONResponse(content=result)

# ROUTE GET DATA Satuan Konversi BY ID
@routerSatuanKonversi.get("/{produk_id}/satuan_konversi/{konversi_id}", response_model=SatuanKonversiSingleSchema, responses=example_responses)
async def get_satuan_konversi(
    http_request: Request,
    timestamp_data: bool = Query(False, description="Jika true, JSON akan disertakan detail timestamp."),
    produk_id: int = Path(..., description="ID dari API GET `/master/produk` (get_all_produk) -> key `produk_id` "),
    konversi_id: int = Path(..., description="ID dari API GET `/satuan_konversi` (get_all_satuan_konversi) -> key `konversi_id` "),
    db: Session = Depends(get_db),
    identity: UsersReqSchema = Depends(get_current_user),
):
    # Panggil pengecekan produk
    check_data = await check_and_return_produk(db, produk_id, http_request)
    if check_data:
        return check_data  # Jika produk tidak ditemukan, langsung return JSONResponse    
        
    try:
        data_satuan_konversi = await select_satuan_konversi_by_id(db, produk_id=produk_id, konversi_id=konversi_id, timestamp_data=timestamp_data)
        if not data_satuan_konversi:
            result = await show_not_found(http_request=http_request, status_code=404, error=f"Produk ID {produk_id} dengan Satuan Konversi ID {konversi_id} tidak ditemukan atau tidak aktif.")
        else:
            result = await show_success(data=data_satuan_konversi, http_request=http_request, status_code=status.HTTP_200_OK)

        # Return result['status']['code'] akan dikembalikan sesuai yang dikirim diatas,
        return JSONResponse(content=result, status_code=result['status']['code'])
    except Exception as e:
        logging.error(f"Exception single_list_satuan_konversi: {e}")
        result = show_bad_response(error=str(e), http_request=http_request)
        return JSONResponse(content=result)

# ROUTE CREATE DATA Satuan Konversi
@routerSatuanKonversi.post("/{produk_id}/satuan_konversi", response_model=SatuanKonversiSingleSchema, responses=example_responses)
async def create_satuan_konversi(
    http_request: Request,
    bt: BackgroundTasks,
    request: SatuanKonversiReqSchema,
    produk_id: int = Path(..., description="ID dari API GET `/master/produk` (get_all_produk) -> key `produk_id` "),
    db: Session = Depends(get_db),
    identity: UsersReqSchema = Depends(get_current_user),
):
    
    """
        **Catatan:**

        - `konversi_satuan`: ID dari API GET `/satuan` (get_all_satuan) → key `satuan_id` \n
        - `konversi_sku`: SKU unik (string, opsional) \n
        - `konversi_nilai`: Nilai faktor konversi dari satuan dasar ke satuan ini (float, default 0.0) \n
        - `konversi_harga`: Harga konversi per satuan ini (float, default 0.0) \n
        - `konversi_keterangan`: Keterangan tambahan mengenai konversi (string, opsional) \n
        - `konversi_aktif`: ENUM pilihan `'Aktif'` / `'Tidak Aktif'` (default: `'Aktif'`) \n
        - `konversi_default`: ENUM pilihan `'true'` / `'false'` untuk menandai apakah ini satuan utama (default: `'false'`) \n
    """

    # Panggil pengecekan produk
    check_data = await check_and_return_produk(db, produk_id, http_request)
    if check_data:
        return check_data  # Jika produk tidak ditemukan, langsung return JSONResponse
        
    check_data_produk_satuan = await check_and_return_produk_satuan(db, produk_id=produk_id, satuan_id=request.konversi_satuan, http_request=http_request)
    if check_data_produk_satuan:
        return check_data_produk_satuan  # Jika produk & satuan sama, langsung return JSONResponse
        
    try:
        new_satuan_konversi = await create_data_satuan_konversi(db=db, produk_id=produk_id, satuan_konversi_data_create=request, identity=identity)
        if new_satuan_konversi:
            result = await show_success(data=new_satuan_konversi, http_request=http_request, code_message='createTrue', status_code=status.HTTP_201_CREATED)
        else:
            result = await show_success(http_request=http_request, code_message='createFalse', status_code=status.HTTP_422_UNPROCESSABLE_ENTITY)
            
        return JSONResponse(content=result, status_code=result['status']['code'])
    except Exception as e:
        logging.error(f"Exception create_satuan_konversi: {e}")
        result = show_bad_response(error=str(e), http_request=http_request)
        return JSONResponse(content=result, status_code=result['status']['code'])

# ROUTE UPDATE DATA Satuan Konversi
@routerSatuanKonversi.put("/{produk_id}/satuan_konversi/{konversi_id}", response_model=SatuanKonversiSingleSchema, responses=example_responses)
async def update_satuan_konversi(
    http_request: Request,
    request: SatuanKonversiReqSchema,
    produk_id: int = Path(..., description="ID dari API GET `/master/produk` (get_all_produk) -> key `produk_id` "),
    konversi_id: int = Path(..., description="ID dari API GET `/satuan_konversi` (get_all_satuan_konversi) -> key `konversi_id` "),
    db: Session = Depends(get_db),
    identity: UsersReqSchema = Depends(get_current_user),
):
    
    """
        **Catatan:**

        - `konversi_satuan`: ID dari API GET `/satuan` (get_all_satuan) → key `satuan_id` \n
        - `konversi_sku`: SKU unik (string, opsional) \n
        - `konversi_nilai`: Nilai faktor konversi dari satuan dasar ke satuan ini (float, default 0.0) \n
        - `konversi_harga`: Harga konversi per satuan ini (float, default 0.0) \n
        - `konversi_keterangan`: Keterangan tambahan mengenai konversi (string, opsional) \n
        - `konversi_aktif`: ENUM pilihan `'Aktif'` / `'Tidak Aktif'` (default: `'Aktif'`) \n
        - `konversi_default`: ENUM pilihan `'true'` / `'false'` untuk menandai apakah ini satuan utama (default: `'false'`) \n
    """

    # Panggil pengecekan produk
    check_data = await check_and_return_produk(db, produk_id, http_request)
    if check_data:
        return check_data  # Jika produk tidak ditemukan, langsung return JSONResponse
    
    check_data_produk_satuan = await check_and_return_produk_satuan(db, produk_id=produk_id, satuan_id=request.konversi_satuan, http_request=http_request, exclude_konversi_id=konversi_id)
    if check_data_produk_satuan:
        return check_data_produk_satuan  # Jika produk & satuan sama, langsung return JSONResponse
        
    try:
        check_data_satuan_konversi = await check_satuan_konversi(db, produk_id=produk_id, konversi_id=konversi_id)
        if not check_data_satuan_konversi:
            result = await show_not_found(http_request=http_request, status_code=404, error=f"Produk ID {produk_id} dengan Satuan Konversi ID {konversi_id} tidak ditemukan atau tidak aktif.")
        else:
            data_satuan_konversi = await update_data_satuan_konversi(db=db, produk_id=produk_id, konversi_id=konversi_id, satuan_konversi_data_update=request, identity=identity)
            result = await show_success(data=data_satuan_konversi, http_request=http_request, status_code=status.HTTP_200_OK)

        # Return result['status']['code'] akan dikembalikan sesuai yang dikirim diatas,
        return JSONResponse(content=result, status_code=result['status']['code'])
    except Exception as e:
        logging.error(f"Exception update_satuan_konversi: {e}")
        result = show_bad_response(error=str(e), http_request=http_request)
        return JSONResponse(content=result)
    
# ROUTE UPDATE PATCH DATA Satuan Konversi
@routerSatuanKonversi.patch("/{produk_id}/satuan_konversi/{konversi_id}", response_model=SatuanKonversiSingleSchema, responses=example_responses)
async def partial_update_satuan_konversi(
    http_request: Request,
    request: SatuanKonversiPatchSchema,
    produk_id: int = Path(..., description="ID dari API GET `/master/produk` (get_all_produk) -> key `produk_id` "),
    konversi_id: int = Path(..., description="ID dari API GET `/satuan_konversi` (get_all_satuan_konversi) -> key `konversi_id` "),
    db: Session = Depends(get_db),
    identity: UsersReqSchema = Depends(get_current_user),
):
    
    """
        **Catatan:**

        - `konversi_satuan`: ID dari API GET `/satuan` (get_all_satuan) → key `satuan_id` \n
        - `konversi_sku`: SKU unik (string, opsional) \n
        - `konversi_nilai`: Nilai faktor konversi dari satuan dasar ke satuan ini (float, default 0.0) \n
        - `konversi_harga`: Harga konversi per satuan ini (float, default 0.0) \n
        - `konversi_keterangan`: Keterangan tambahan mengenai konversi (string, opsional) \n
        - `konversi_aktif`: ENUM pilihan `'Aktif'` / `'Tidak Aktif'` (default: `'Aktif'`) \n
        - `konversi_default`: ENUM pilihan `'true'` / `'false'` untuk menandai apakah ini satuan utama (default: `'false'`) \n
    """

    # Panggil pengecekan produk
    check_data = await check_and_return_produk(db, produk_id, http_request)
    if check_data:
        return check_data  # Jika produk tidak ditemukan, langsung return JSONResponse
    
    check_data_produk_satuan = await check_and_return_produk_satuan(db, produk_id=produk_id, satuan_id=request.konversi_satuan, http_request=http_request, exclude_konversi_id=konversi_id)
    if check_data_produk_satuan:
        return check_data_produk_satuan  # Jika produk & satuan sama, langsung return JSONResponse
        
    try:
        check_data_satuan_konversi = await check_satuan_konversi(db, produk_id=produk_id, konversi_id=konversi_id)
        if not check_data_satuan_konversi:
            result = await show_not_found(http_request=http_request, status_code=404, error=f"Produk ID {produk_id} dengan Satuan Konversi ID {konversi_id} tidak ditemukan atau tidak aktif.")
        else:
            data_satuan_konversi = await partial_update_data_satuan_konversi(db=db, produk_id=produk_id, konversi_id=konversi_id, satuan_konversi_data_update=request.dict(exclude_unset=True), identity=identity)
            result = await show_success(data=data_satuan_konversi, http_request=http_request, status_code=status.HTTP_200_OK)

        # Return result['status']['code'] akan dikembalikan sesuai yang dikirim diatas,
        return JSONResponse(content=result, status_code=result['status']['code'])
    except Exception as e:
        logging.error(f"Exception update_patch_satuan_konversi: {e}")
        result = show_bad_response(error=str(e), http_request=http_request)
        return JSONResponse(content=result)

# ROUTE DELETE DATA Satuan Konversi
@routerSatuanKonversi.delete("/{produk_id}/satuan_konversi/{konversi_id}", response_model=SatuanKonversiSingleSchema, responses=example_responses)
async def delete_satuan_konversi(
    http_request: Request,
    produk_id: int = Path(..., description="ID dari API GET `/master/produk` (get_all_produk) -> key `produk_id` "),
    konversi_id: int = Path(..., description="ID dari API GET `/satuan_konversi` (get_all_satuan_konversi) -> key `konversi_id` "),
    db: Session = Depends(get_db),
    identity: UsersReqSchema = Depends(get_current_user),
):
    
    # Panggil pengecekan produk
    check_data = await check_and_return_produk(db, produk_id, http_request)
    if check_data:
        return check_data  # Jika produk tidak ditemukan, langsung return JSONResponse
    
    try:
        check_data_satuan_konversi = await check_satuan_konversi(db, produk_id=produk_id, konversi_id=konversi_id)
        if not check_data_satuan_konversi:
            result = await show_not_found(http_request=http_request, status_code=404, error=f"Produk ID {produk_id} dengan Satuan Konversi ID {konversi_id} tidak ditemukan atau tidak aktif.")
        else:
            deleted_data_satuan_konversi = await delete_data_satuan_konversi(db=db, produk_id=produk_id, konversi_id=konversi_id, identity=identity)
            result = await show_success(data=deleted_data_satuan_konversi, http_request=http_request, status_code=status.HTTP_200_OK)

        # Return result['status']['code'] akan dikembalikan sesuai yang dikirim diatas,
        return JSONResponse(content=result, status_code=result['status']['code'])
    except Exception as e:
        logging.error(f"Exception delete_satuan_konversi: {e}")
        result = show_bad_response(error=str(e), http_request=http_request)
        return JSONResponse(content=result)
    
# END CODE ROUTE Satuan Konversi