# ============================================= Start Noted Router ===================================
# Author : PT. Dapur Perangkat Lunak Indonesia | KoffieSoft Group | https://www.koffiesoft.com/ | info@koffiesoft.com
# 1. @routerProduk.get("/daftar", response_model=ProdukListSchema) >> routerProduk = abstrack class dari APIRouter. dipanggil di router/api_router.py
# 2. responseHandle = ResponseHandle() >> responseHandle = abstrack class standart dari core/utils/response_handle.py
# 3. async def get_daftar_produk() >> Nama function akan dijadikan title di main.py, misal get_daftar_produk
# 4. identity: UsersReqSchema = Depends(get_current_user),
#   - async def sample_function(
#       identity: UsersReqSchema = Depends(get_current_user) >> parameter `identity : ` Ini digunakan MENGGUNAKAN / TIDAK TOKEN saat akses api
# 5. Contoh rq ke file crud.py : get_daftar_produk && get_crud_daftar_produk dibedakan >> supaya memudahkan klik function
# 6. 'http_request: Request` >> menginisialisasikan scarlete.object untuk mengambil request awal dari http
# 7. request: ProdukReqSchema = Depends(ProdukReqSchema.as_form)
#       - request: ProdukReqSchema = Depends(ProdukReqSchema.as_form) -> type data form
#       - request: ProdukReqSchema = application/json
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
from core.modules.produk.crud.produk_crud import (
    get_crud_daftar_produk,
    select_produk_by_id,
    create_data_produk,
    update_data_produk,
    partial_update_data_produk,
    delete_data_produk
)
from core.modules.users.schema.users_schema import (
    UsersReqSchema,
)
from core.modules.produk.schema.produk_schema import (
    ProdukBaseDataSchema,
    ProdukRequestListSchema,
    ProdukListSchema,
    ProdukReqSchema,
    ProdukPutSchema,
    ProdukPatchSchema,
    ProdukSingleSchema
)
from core.utils.oauth2 import get_current_user
from core.shared.check_data_model import (
    check_produk,
    check_produk_nama
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

# START CODE ROUTE PRODUK
routerProduk = APIRouter(tags=["Master - Produk"], prefix="/produk")

example_responses = get_example_responses(status_codes=[401, 404, 405, 422, 500])

# ROUTE LIST & SEARCH DATA PRODUK
@routerProduk.get("", response_model=ProdukListSchema, responses=example_responses)
async def get_all_produk(
    http_request: Request,
    request: ProdukRequestListSchema = Depends(ProdukRequestListSchema.as_form),
    identity: UsersReqSchema = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    try:
        daftar = await get_crud_daftar_produk(db=db, request=request)

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
        logging.error(f"Exception list_produk: {e}")
        result = show_bad_response(error=str(e), http_request=http_request)
        return JSONResponse(content=jsonable_encoder(result))

# ROUTE GET DATA PRODUK BY ID
@routerProduk.get("/{produk_id}", response_model=ProdukSingleSchema, responses=example_responses)
async def get_produk(
    http_request: Request,
    produk_id: int = Path(..., description="ID dari API GET `/master/produk` (get_all_produk) -> key `produk_id` "),
    timestamp_data: bool = Query(False, description="Jika true, JSON akan disertakan detail timestamp."),
    db: Session = Depends(get_db),
    identity: UsersReqSchema = Depends(get_current_user),
):
    try:
        data_produk = await select_produk_by_id(db, produk_id=produk_id, timestamp_data=timestamp_data)
        if not data_produk:
            result = await show_not_found(http_request=http_request, status_code=404)
        else:
            result = await show_success(data=data_produk, http_request=http_request, status_code=status.HTTP_200_OK)

        # Return result['status']['code'] akan dikembalikan sesuai yang dikirim diatas,
        return JSONResponse(content=jsonable_encoder(result), status_code=result['status']['code'])
    except Exception as e:
        logging.error(f"Exception single_list_produk: {e}")
        result = show_bad_response(error=str(e), http_request=http_request)
        return JSONResponse(content=jsonable_encoder(result))

# ROUTE CREATE DATA PRODUK
@routerProduk.post("", response_model=ProdukSingleSchema, responses=example_responses)
async def create_produk(
    http_request: Request,
    bt: BackgroundTasks,
    request: ProdukReqSchema,
    db: Session = Depends(get_db),
    identity: UsersReqSchema = Depends(get_current_user),
):
    
    """
        **Catatan:**

        - `produk_id` : Primary key produk. Auto Increment (tidak perlu diisi saat create).  \n
        - `produk_kode` : Kode unik produk. Wajib diisi. Maksimal 20 karakter.  \n
        - `produk_sku` : SKU (Stock Keeping Unit), satuan terkecil untuk informasi. *(Opsional)*  \n
        - `produk_group` : ID grup produk utama. Foreign key dari tabel `produk_group` -> kolom `group_id`. *(Opsional)*  \n
        - `produk_nama` : Nama produk. Wajib diisi. Maksimal 250 karakter.  \n
        - `produk_satuan` : ID satuan produk. Foreign key dari tabel `satuan` -> kolom `satuan_id`. *(Opsional)*  \n
        - `produk_harga` : Harga satuan default. Float. Default: `0.0`.  \n
        - `produk_diskon` : Diskon dalam persentase. Decimal(10,2). Default: `0.00`.  \n
        - `produk_diskon_rp` : Diskon dalam rupiah. Float. Default: `0.0`.  \n
        - `produk_aktif` : Status produk. ENUM: `Aktif` / `Tidak Aktif`. Default: `Aktif`.  \n
        - `produk_keterangan` : Catatan tambahan mengenai produk. Maksimal 500 karakter. *(Opsional)*  \n
    """
        
    try:
        if request.produk_nama is not None:
            user = await check_produk_nama(db, produk_nama=request.produk_nama)
            if user:
                result = await show_bad_request(http_request=http_request, error=f"Produk Dengan Nama {request.produk_nama} Sudah terdaftar sebelumnya", status_code=status.HTTP_400_BAD_REQUEST)
                return JSONResponse(content=result, status_code=result['status']['code'])
            
        new_produk = await create_data_produk(db=db, produk_data_create=request, identity=identity)
        if new_produk:
            result = await show_success(data=new_produk, http_request=http_request, code_message='createTrue', status_code=status.HTTP_201_CREATED)
        else:
            result = await show_success(http_request=http_request, code_message='createFalse', status_code=status.HTTP_422_UNPROCESSABLE_ENTITY)
            
        return JSONResponse(content=jsonable_encoder(result), status_code=result['status']['code'])
    except Exception as e:
        logging.error(f"Exception create_produk: {e}")
        result = show_bad_response(error=str(e), http_request=http_request)
        return JSONResponse(content=jsonable_encoder(result), status_code=result['status']['code'])

# ROUTE UPDATE DATA PRODUK
@routerProduk.put("/{produk_id}", response_model=ProdukSingleSchema, responses=example_responses)
async def update_produk(
    http_request: Request,
    request: ProdukPutSchema,
    produk_id: int = Path(..., description="ID dari API GET `/master/produk` (get_all_produk) -> key `produk_id` "),
    db: Session = Depends(get_db),
    identity: UsersReqSchema = Depends(get_current_user),
):
    
    """
        **Catatan:**

        - `produk_id` : Primary key produk. Auto Increment (tidak perlu diisi saat create).  \n
        - `produk_kode` : Kode unik produk. Wajib diisi. Maksimal 20 karakter.  \n
        - `produk_sku` : SKU (Stock Keeping Unit), satuan terkecil untuk informasi. *(Opsional)*  \n
        - `produk_group` : ID grup produk utama. Foreign key dari tabel `produk_group` -> kolom `group_id`. *(Opsional)*  \n
        - `produk_nama` : Nama produk. Wajib diisi. Maksimal 250 karakter.  \n
        - `produk_satuan` : ID satuan produk. Foreign key dari tabel `satuan` -> kolom `satuan_id`. *(Opsional)*  \n
        - `produk_harga` : Harga satuan default. Float. Default: `0.0`.  \n
        - `produk_diskon` : Diskon dalam persentase. Decimal(10,2). Default: `0.00`.  \n
        - `produk_diskon_rp` : Diskon dalam rupiah. Float. Default: `0.0`.  \n
        - `produk_aktif` : Status produk. ENUM: `Aktif` / `Tidak Aktif`. Default: `Aktif`.  \n
        - `produk_keterangan` : Catatan tambahan mengenai produk. Maksimal 500 karakter. *(Opsional)*  \n
    """
        
    try:
        if request.produk_nama is not None:
            user = await check_produk_nama(db, produk_nama=request.produk_nama, exclude_produk_id=produk_id)
            if user:
                result = await show_bad_request(http_request=http_request, error=f"Produk Dengan Nama {request.produk_nama} Sudah terdaftar sebelumnya", status_code=status.HTTP_400_BAD_REQUEST)
                return JSONResponse(content=result, status_code=result['status']['code'])
    
        check_data_produk = await check_produk(db, produk_id=produk_id)
        if not check_data_produk:
            result = await show_not_found(http_request=http_request, status_code=404)
        else:
            data_produk = await update_data_produk(db=db, produk_id=produk_id, produk_data_update=request, identity=identity)
            result = await show_success(data=data_produk, http_request=http_request, status_code=status.HTTP_200_OK)

        # Return result['status']['code'] akan dikembalikan sesuai yang dikirim diatas,
        return JSONResponse(content=jsonable_encoder(result), status_code=result['status']['code'])
    except Exception as e:
        logging.error(f"Exception update_produk: {e}")
        result = show_bad_response(error=str(e), http_request=http_request)
        return JSONResponse(content=jsonable_encoder(result))

# ROUTE UPDATE PATCH DATA PRODUK
@routerProduk.patch("/{produk_id}", response_model=ProdukSingleSchema, responses=example_responses)
async def partial_update_produk(
    http_request: Request,
    request: ProdukPatchSchema,
    produk_id: int = Path(..., description="ID dari API GET `/master/produk` (get_all_produk) -> key `produk_id` "),
    db: Session = Depends(get_db),
    identity: UsersReqSchema = Depends(get_current_user),
):
    
    """
        **Catatan:**

        - `produk_id` : Primary key produk. Auto Increment (tidak perlu diisi saat create).  \n
        - `produk_kode` : Kode unik produk. Wajib diisi. Maksimal 20 karakter.  \n
        - `produk_sku` : SKU (Stock Keeping Unit), satuan terkecil untuk informasi. *(Opsional)*  \n
        - `produk_group` : ID grup produk utama. Foreign key dari tabel `produk_group` -> kolom `group_id`. *(Opsional)*  \n
        - `produk_nama` : Nama produk. Wajib diisi. Maksimal 250 karakter.  \n
        - `produk_satuan` : ID satuan produk. Foreign key dari tabel `satuan` -> kolom `satuan_id`. *(Opsional)*  \n
        - `produk_harga` : Harga satuan default. Float. Default: `0.0`.  \n
        - `produk_diskon` : Diskon dalam persentase. Decimal(10,2). Default: `0.00`.  \n
        - `produk_diskon_rp` : Diskon dalam rupiah. Float. Default: `0.0`.  \n
        - `produk_aktif` : Status produk. ENUM: `Aktif` / `Tidak Aktif`. Default: `Aktif`.  \n
        - `produk_keterangan` : Catatan tambahan mengenai produk. Maksimal 500 karakter. *(Opsional)*  \n
    """
        
    try:
        check_data_produk = await check_produk(db, produk_id=produk_id)
        if not check_data_produk:
            result = await show_not_found(http_request=http_request, status_code=404)
        else:
            data_produk = await partial_update_data_produk(db=db, produk_id=produk_id, produk_data_update=request.dict(exclude_unset=True), identity=identity)
            result = await show_success(data=data_produk, http_request=http_request, status_code=status.HTTP_200_OK)

        # Return result['status']['code'] akan dikembalikan sesuai yang dikirim diatas,
        return JSONResponse(content=jsonable_encoder(result), status_code=result['status']['code'])
    except Exception as e:
        logging.error(f"Exception update_patch_produk: {e}")
        result = show_bad_response(error=str(e), http_request=http_request)
        return JSONResponse(content=jsonable_encoder(result))

# ROUTE DELETE DATA PRODUK
@routerProduk.delete("/{produk_id}", response_model=ProdukSingleSchema, responses=example_responses)
async def delete_produk(
    http_request: Request,
    produk_id: int = Path(..., description="ID dari API GET `/master/produk` (get_all_produk) -> key `produk_id` "),
    db: Session = Depends(get_db),
    identity: UsersReqSchema = Depends(get_current_user),
):
    try:
        check_data_produk = await check_produk(db, produk_id=produk_id)
        if not check_data_produk:
            result = await show_not_found(http_request=http_request, status_code=404)
        else:
            deleted_data_produk = await delete_data_produk(db=db, produk_id=produk_id, identity=identity)
            result = await show_success(data=deleted_data_produk, http_request=http_request, status_code=status.HTTP_200_OK)

        # Return result['status']['code'] akan dikembalikan sesuai yang dikirim diatas,
        return JSONResponse(content=jsonable_encoder(result), status_code=result['status']['code'])
    except Exception as e:
        logging.error(f"Exception delete_produk: {e}")
        result = show_bad_response(error=str(e), http_request=http_request)
        return JSONResponse(content=jsonable_encoder(result))

# END CODE ROUTE PRODUK