# ============================================= Start Noted Router ===================================
# Author : Abdul Rohman Masrifan | masrifan26@gamil.com
# 1. @routerProdukBarcode.get("/daftar", response_model=ProdukBarcodeListSchema) >> routerProdukBarcode = abstrack class dari APIRouter. dipanggil di router/api_router.py
# 2. responseHandle = ResponseHandle() >> responseHandle = abstrack class standart dari core/utils/response_handle.py
# 3. async def get_daftar_produk_barcode() >> Nama function akan dijadikan title di main.py, misal get_daftar_produk_barcode
# 4. identity: UsersReqSchema = Depends(get_current_user),
#   - async def sample_function(
#       identity: UsersReqSchema = Depends(get_current_user) >> parameter `identity : ` Ini digunakan MENGGUNAKAN / TIDAK TOKEN saat akses api
# 5. Contoh rq ke file crud.py : get_daftar_produk_barcode && get_crud_daftar_produk_barcode dibedakan >> supaya memudahkan klik function
# 6. 'http_request: Request` >> menginisialisasikan scarlete.object untuk mengambil request awal dari http
# 7. request: ProdukBarcodeReqSchema = Depends(ProdukBarcodeReqSchema.as_form)
#       - request: ProdukBarcodeReqSchema = Depends(ProdukBarcodeReqSchema.as_form) -> type data form
#       - request: ProdukBarcodeReqSchema = application/json
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
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from database import get_db
from core.modules.master.produk_barcode.crud.produk_barcode_crud import (
    get_crud_daftar_produk_barcode,
    select_produk_barcode_by_id,
    select_produk_barcode_by_barcode,
    create_data_produk_barcode,
    update_data_produk_barcode,
    partial_update_data_produk_barcode,
    delete_data_produk_barcode
)
from core.modules.users.schema.users_schema import (
    UsersReqSchema,
)
from core.modules.master.produk_barcode.schema.produk_barcode_schema import (
    ProdukBarcodeBaseDataSchema,
    ProdukBarcodeRequestListSchema,
    ProdukBarcodeListSchema,
    ProdukBarcodeReqSchema,
    ProdukBarcodePutSchema,
    ProdukBarcodePatchSchema,
    ProdukBarcodeSingleSchema
)
from core.utils.oauth2 import get_current_user
from core.shared.check_data_model import (
    check_produk_barcode,
    check_product_by_barcode
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

# START CODE ROUTE PRODUK BARCODE 
routerProdukBarcode = APIRouter(tags=["Master - Produk Barcode"], prefix="/produk_barcode")

example_responses = get_example_responses(status_codes=[401, 404, 405, 422, 500])

# ROUTE LIST & SEARCH DATA PRODUK BARCODE 
@routerProdukBarcode.get("", response_model=ProdukBarcodeListSchema, responses=example_responses)
async def get_all_produk_barcode(
    http_request: Request,
    request: ProdukBarcodeRequestListSchema = Depends(ProdukBarcodeRequestListSchema.as_form),
    identity: UsersReqSchema = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    try:
        daftar = await get_crud_daftar_produk_barcode(db=db, request=request)

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
        logging.error(f"Exception list_produk_barcode: {e}")
        result = show_bad_response(error=str(e), http_request=http_request)
        return JSONResponse(content=result)

# ROUTE GET DATA PRODUK BARCODE  BY ID
@routerProdukBarcode.get("/{productId}", response_model=ProdukBarcodeSingleSchema, responses=example_responses)
async def get_produk_barcode(
    http_request: Request,
    timestamp_data: bool = Query(False, description="Jika true, JSON akan disertakan detail timestamp."),
    productId: int = Path(..., description="ID dari API GET `/produk_barcode` (get_all_produk_barcode) -> key `productId` "),
    db: Session = Depends(get_db),
    identity: UsersReqSchema = Depends(get_current_user),
):
    try:
        data_produk_barcode = await select_produk_barcode_by_id(db, productId=productId, timestamp_data=timestamp_data)
        if not data_produk_barcode:
            result = await show_not_found(http_request=http_request, status_code=404)
        else:
            result = await show_success(data=data_produk_barcode, http_request=http_request, status_code=status.HTTP_200_OK)

        # Return result['status']['code'] akan dikembalikan sesuai yang dikirim diatas,
        return JSONResponse(content=result, status_code=result['status']['code'])
    except Exception as e:
        logging.error(f"Exception single_list_produk_barcode: {e}")
        result = show_bad_response(error=str(e), http_request=http_request)
        return JSONResponse(content=result)
    
@routerProdukBarcode.get("/by_barcode/{productBarcode}", response_model=ProdukBarcodeSingleSchema, responses=example_responses)
async def get_produk_barcode(
    http_request: Request,
    timestamp_data: bool = Query(False, description="Jika true, JSON akan disertakan detail timestamp."),
    productBarcode: int = Path(..., description="ID dari API GET `/produk_barcode` (get_all_produk_barcode) -> key `productBarcode` "),
    db: Session = Depends(get_db),
    identity: UsersReqSchema = Depends(get_current_user),
):
    try:
        data_produk_barcode = await select_produk_barcode_by_barcode(db, productBarcode=productBarcode, timestamp_data=timestamp_data)
        if not data_produk_barcode:
            result = await show_not_found(http_request=http_request, status_code=404)
        else:
            result = await show_success(data=data_produk_barcode, http_request=http_request, status_code=status.HTTP_200_OK)

        # Return result['status']['code'] akan dikembalikan sesuai yang dikirim diatas,
        return JSONResponse(content=result, status_code=result['status']['code'])
    except Exception as e:
        logging.error(f"Exception single_list_produk_barcode: {e}")
        result = show_bad_response(error=str(e), http_request=http_request)
        return JSONResponse(content=result)

# ROUTE CREATE DATA PRODUK BARCODE 
@routerProdukBarcode.post("", response_model=ProdukBarcodeSingleSchema, responses=example_responses)
async def create_produk_barcode(
    http_request: Request,
    bt: BackgroundTasks,
    request: ProdukBarcodeReqSchema,
    db: Session = Depends(get_db),
    identity: UsersReqSchema = Depends(get_current_user),
):
    
    """
        **Catatan:** 

        `aktif`: ENUM pilihan `Aktif`/`Tidak Aktif` \n
    """

        
    try:
        if request.productBarcode is not None:
            produk_barcode_check = await check_product_by_barcode(db, productBarcode=request.productBarcode)
            if produk_barcode_check:
                result = await show_bad_request(http_request=http_request, error=f"Kode ProdukBarcode {request.productBarcode} Sudah terdaftar sebelumnya", status_code=status.HTTP_400_BAD_REQUEST)
                return JSONResponse(content=result, status_code=result['status']['code'])
            
        new_produk_barcode = await create_data_produk_barcode(db=db, produk_barcode_data_create=request, identity=identity)
        if new_produk_barcode:
            result = await show_success(data=new_produk_barcode, http_request=http_request, code_message='createTrue', status_code=status.HTTP_201_CREATED)
        else:
            result = await show_success(http_request=http_request, code_message='createFalse', status_code=status.HTTP_422_UNPROCESSABLE_ENTITY)
            
        return JSONResponse(content=result, status_code=result['status']['code'])
    except Exception as e:
        logging.error(f"Exception create_produk_barcode: {e}")
        result = show_bad_response(error=str(e), http_request=http_request)
        return JSONResponse(content=result, status_code=result['status']['code'])

# ROUTE UPDATE DATA PRODUK BARCODE 
@routerProdukBarcode.put("/{productId}", response_model=ProdukBarcodeSingleSchema, responses=example_responses)
async def update_produk_barcode(
    http_request: Request,
    request: ProdukBarcodePutSchema,
    productId: int = Path(..., description="ID dari API GET `/produk_barcode` (get_all_produk_barcode) -> key `productId` "),
    db: Session = Depends(get_db),
    identity: UsersReqSchema = Depends(get_current_user),
):
    
    """
        **Catatan:** 

        `aktif`: ENUM pilihan `Aktif`/`Tidak Aktif` \n
    """
        
    try:
        if request.productBarcode is not None:
            produk_barcode_check = await check_product_by_barcode(db, productBarcode=request.productBarcode, exclude_id=productId)
            if produk_barcode_check:
                result = await show_bad_request(http_request=http_request, error=f"Kode ProdukBarcode {request.productBarcode} Sudah terdaftar sebelumnya", status_code=status.HTTP_400_BAD_REQUEST)
                return JSONResponse(content=result, status_code=result['status']['code'])
    
        check_data_produk_barcode = await check_produk_barcode(db, productId=productId)
        if not check_data_produk_barcode:
            result = await show_not_found(http_request=http_request, status_code=404)
        else:
            data_produk_barcode = await update_data_produk_barcode(db=db, productId=productId, produk_barcode_data_update=request, identity=identity)
            result = await show_success(data=data_produk_barcode, http_request=http_request, status_code=status.HTTP_200_OK)

        # Return result['status']['code'] akan dikembalikan sesuai yang dikirim diatas,
        return JSONResponse(content=result, status_code=result['status']['code'])
    except Exception as e:
        logging.error(f"Exception update_produk_barcode: {e}")
        result = show_bad_response(error=str(e), http_request=http_request)
        return JSONResponse(content=result)
    
# ROUTE UPDATE PATCH DATA PRODUK BARCODE 
@routerProdukBarcode.patch("/{productId}", response_model=ProdukBarcodeSingleSchema, responses=example_responses)
async def partial_update_produk_barcode(
    http_request: Request,
    request: ProdukBarcodePatchSchema,
    productId: int = Path(..., description="ID dari API GET `/produk_barcode` (get_all_produk_barcode) -> key `productId` "),
    db: Session = Depends(get_db),
    identity: UsersReqSchema = Depends(get_current_user),
):
    
    """
        **Catatan:** 

        `aktif`: ENUM pilihan `Aktif`/`Tidak Aktif` \n
    """
        
    try:
        check_data_produk_barcode = await check_produk_barcode(db, productId=productId)
        if not check_data_produk_barcode:
            result = await show_not_found(http_request=http_request, status_code=404)
        else:
            data_produk_barcode = await partial_update_data_produk_barcode(db=db, productId=productId, produk_barcode_data_update=request.dict(exclude_unset=True), identity=identity)
            result = await show_success(data=data_produk_barcode, http_request=http_request, status_code=status.HTTP_200_OK)

        # Return result['status']['code'] akan dikembalikan sesuai yang dikirim diatas,
        return JSONResponse(content=result, status_code=result['status']['code'])
    except Exception as e:
        logging.error(f"Exception update_patch_produk_barcode: {e}")
        result = show_bad_response(error=str(e), http_request=http_request)
        return JSONResponse(content=result)

# ROUTE DELETE DATA PRODUK BARCODE 
@routerProdukBarcode.delete("/{productId}", response_model=ProdukBarcodeSingleSchema, responses=example_responses)
async def delete_produk_barcode(
    http_request: Request,
    productId: int = Path(..., description="ID dari API GET `/produk_barcode` (get_all_produk_barcode) -> key `productId` "),
    db: Session = Depends(get_db),
    identity: UsersReqSchema = Depends(get_current_user),
):
    try:
        check_data_produk_barcode = await check_produk_barcode(db, productId=productId)
        if not check_data_produk_barcode:
            result = await show_not_found(http_request=http_request, status_code=404)
        else:
            deleted_data_produk_barcode = await delete_data_produk_barcode(db=db, productId=productId, identity=identity)
            result = await show_success(data=deleted_data_produk_barcode, http_request=http_request, status_code=status.HTTP_200_OK)

        # Return result['status']['code'] akan dikembalikan sesuai yang dikirim diatas,
        return JSONResponse(content=result, status_code=result['status']['code'])
    except Exception as e:
        logging.error(f"Exception delete_produk_barcode: {e}")
        result = show_bad_response(error=str(e), http_request=http_request)
        return JSONResponse(content=result)
    
# END CODE ROUTE PRODUK BARCODE 