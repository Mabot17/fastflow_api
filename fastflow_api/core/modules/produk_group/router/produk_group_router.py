# ============================================= Start Noted Router ===================================
# Author : PT. Dapur Perangkat Lunak Indonesia | KoffieSoft Group | https://www.koffiesoft.com/ | info@koffiesoft.com
# 1. @routerProdukGroup.get("/daftar", response_model=ProdukGroupListSchema) >> routerProdukGroup = abstrack class dari APIRouter. dipanggil di router/api_router.py
# 2. responseHandle = ResponseHandle() >> responseHandle = abstrack class standart dari core/utils/response_handle.py
# 3. async def get_daftar_produk_group() >> Nama function akan dijadikan title di main.py, misal get_daftar_produk_group
# 4. identity: UsersReqSchema = Depends(get_current_user),
#   - async def sample_function(
#       identity: UsersReqSchema = Depends(get_current_user) >> parameter `identity : ` Ini digunakan MENGGUNAKAN / TIDAK TOKEN saat akses api
# 5. Contoh rq ke file crud.py : get_daftar_produk_group && get_crud_daftar_produk_group dibedakan >> supaya memudahkan klik function
# 6. 'http_request: Request` >> menginisialisasikan scarlete.object untuk mengambil request awal dari http
# 7. request: ProdukGroupReqSchema = Depends(ProdukGroupReqSchema.as_form)
#       - request: ProdukGroupReqSchema = Depends(ProdukGroupReqSchema.as_form) -> type data form
#       - request: ProdukGroupReqSchema = application/json
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
from core.modules.produk_group.crud.produk_group_crud import (
    get_crud_daftar_produk_group,
    select_produk_group_by_id,
    create_data_produk_group,
    update_data_produk_group,
    partial_update_data_produk_group,
    delete_data_produk_group
)
from core.modules.users.schema.users_schema import (
    UsersReqSchema,
)
from core.modules.produk_group.schema.produk_group_schema import (
    ProdukGroupBaseDataSchema,
    ProdukGroupRequestListSchema,
    ProdukGroupListSchema,
    ProdukGroupReqSchema,
    ProdukGroupPutSchema,
    ProdukGroupPatchSchema,
    ProdukGroupSingleSchema
)
from core.utils.oauth2 import get_current_user
from core.shared.check_data_model import (
    check_produk_group,
    check_group_kode
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

# START CODE ROUTE PRODUK GROUP
routerProdukGroup = APIRouter(tags=["Master - Produk Group"], prefix="/produk_group")

example_responses = get_example_responses(status_codes=[401, 404, 405, 422, 500])

# ROUTE LIST & SEARCH DATA PRODUK GROUP
@routerProdukGroup.get("", response_model=ProdukGroupListSchema, responses=example_responses)
async def get_all_produk_group(
    http_request: Request,
    request: ProdukGroupRequestListSchema = Depends(ProdukGroupRequestListSchema.as_form),
    identity: UsersReqSchema = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    try:
        daftar = await get_crud_daftar_produk_group(db=db, request=request)

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
        logging.error(f"Exception list_produk_group: {e}")
        result = show_bad_response(error=str(e), http_request=http_request)
        return JSONResponse(content=result)

# ROUTE GET DATA PRODUK GROUP BY ID
@routerProdukGroup.get("/{group_id}", response_model=ProdukGroupSingleSchema, responses=example_responses)
async def get_produk_group(
    http_request: Request,
    timestamp_data: bool = Query(False, description="Jika true, JSON akan disertakan detail timestamp."),
    group_id: int = Path(..., description="ID dari API GET `/master/produk_group` (get_all_produk_group) -> key `group_id` "),
    db: Session = Depends(get_db),
    identity: UsersReqSchema = Depends(get_current_user),
):
    try:
        data_produk_group = await select_produk_group_by_id(db, group_id=group_id, timestamp_data=timestamp_data)
        if not data_produk_group:
            result = await show_not_found(http_request=http_request, status_code=404)
        else:
            result = await show_success(data=data_produk_group, http_request=http_request, status_code=status.HTTP_200_OK)

        # Return result['status']['code'] akan dikembalikan sesuai yang dikirim diatas,
        return JSONResponse(content=result, status_code=result['status']['code'])
    except Exception as e:
        logging.error(f"Exception single_list_produk_group: {e}")
        result = show_bad_response(error=str(e), http_request=http_request)
        return JSONResponse(content=result)

# ROUTE CREATE DATA PRODUK GROUP
@routerProdukGroup.post("", response_model=ProdukGroupSingleSchema, responses=example_responses)
async def create_produk_group(
    http_request: Request,
    bt: BackgroundTasks,
    request: ProdukGroupReqSchema,
    db: Session = Depends(get_db),
    identity: UsersReqSchema = Depends(get_current_user),
):
    
    """
        **Catatan:** 

        `group_aktif`: ENUM pilihan `Aktif`/`Tidak Aktif` \n
    """

        
    try:
        if request.group_kode is not None:
            produk_group_check = await check_group_kode(db, group_kode=request.group_kode)
            if produk_group_check:
                result = await show_bad_request(http_request=http_request, error=f"Kode ProdukGroup {request.group_kode} Sudah terdaftar sebelumnya", status_code=status.HTTP_400_BAD_REQUEST)
                return JSONResponse(content=result, status_code=result['status']['code'])
            
        new_produk_group = await create_data_produk_group(db=db, produk_group_data_create=request, identity=identity)
        if new_produk_group:
            result = await show_success(data=new_produk_group, http_request=http_request, code_message='createTrue', status_code=status.HTTP_201_CREATED)
        else:
            result = await show_success(http_request=http_request, code_message='createFalse', status_code=status.HTTP_422_UNPROCESSABLE_ENTITY)
            
        return JSONResponse(content=result, status_code=result['status']['code'])
    except Exception as e:
        logging.error(f"Exception create_produk_group: {e}")
        result = show_bad_response(error=str(e), http_request=http_request)
        return JSONResponse(content=result, status_code=result['status']['code'])

# ROUTE UPDATE DATA PRODUK GROUP
@routerProdukGroup.put("/{group_id}", response_model=ProdukGroupSingleSchema, responses=example_responses)
async def update_produk_group(
    http_request: Request,
    request: ProdukGroupPutSchema,
    group_id: int = Path(..., description="ID dari API GET `/master/produk_group` (get_all_produk_group) -> key `group_id` "),
    db: Session = Depends(get_db),
    identity: UsersReqSchema = Depends(get_current_user),
):
    
    """
        **Catatan:** 

        `group_aktif`: ENUM pilihan `Aktif`/`Tidak Aktif` \n
    """
        
    try:
        if request.group_kode is not None:
            produk_group_check = await check_group_kode(db, group_kode=request.group_kode, exclude_group_id=group_id)
            if produk_group_check:
                result = await show_bad_request(http_request=http_request, error=f"Kode ProdukGroup {request.group_kode} Sudah terdaftar sebelumnya", status_code=status.HTTP_400_BAD_REQUEST)
                return JSONResponse(content=result, status_code=result['status']['code'])
    
        check_data_produk_group = await check_produk_group(db, group_id=group_id)
        if not check_data_produk_group:
            result = await show_not_found(http_request=http_request, status_code=404)
        else:
            data_produk_group = await update_data_produk_group(db=db, group_id=group_id, produk_group_data_update=request, identity=identity)
            result = await show_success(data=data_produk_group, http_request=http_request, status_code=status.HTTP_200_OK)

        # Return result['status']['code'] akan dikembalikan sesuai yang dikirim diatas,
        return JSONResponse(content=result, status_code=result['status']['code'])
    except Exception as e:
        logging.error(f"Exception update_produk_group: {e}")
        result = show_bad_response(error=str(e), http_request=http_request)
        return JSONResponse(content=result)
    
# ROUTE UPDATE PATCH DATA PRODUK GROUP
@routerProdukGroup.patch("/{group_id}", response_model=ProdukGroupSingleSchema, responses=example_responses)
async def partial_update_produk_group(
    http_request: Request,
    request: ProdukGroupPatchSchema,
    group_id: int = Path(..., description="ID dari API GET `/master/produk_group` (get_all_produk_group) -> key `group_id` "),
    db: Session = Depends(get_db),
    identity: UsersReqSchema = Depends(get_current_user),
):
    
    """
        **Catatan:** 

        `group_aktif`: ENUM pilihan `Aktif`/`Tidak Aktif` \n
    """
        
    try:
        check_data_produk_group = await check_produk_group(db, group_id=group_id)
        if not check_data_produk_group:
            result = await show_not_found(http_request=http_request, status_code=404)
        else:
            data_produk_group = await partial_update_data_produk_group(db=db, group_id=group_id, produk_group_data_update=request.dict(exclude_unset=True), identity=identity)
            result = await show_success(data=data_produk_group, http_request=http_request, status_code=status.HTTP_200_OK)

        # Return result['status']['code'] akan dikembalikan sesuai yang dikirim diatas,
        return JSONResponse(content=result, status_code=result['status']['code'])
    except Exception as e:
        logging.error(f"Exception update_patch_produk_group: {e}")
        result = show_bad_response(error=str(e), http_request=http_request)
        return JSONResponse(content=result)

# ROUTE DELETE DATA PRODUK GROUP
@routerProdukGroup.delete("/{group_id}", response_model=ProdukGroupSingleSchema, responses=example_responses)
async def delete_produk_group(
    http_request: Request,
    group_id: int = Path(..., description="ID dari API GET `/master/produk_group` (get_all_produk_group) -> key `group_id` "),
    db: Session = Depends(get_db),
    identity: UsersReqSchema = Depends(get_current_user),
):
    try:
        check_data_produk_group = await check_produk_group(db, group_id=group_id)
        if not check_data_produk_group:
            result = await show_not_found(http_request=http_request, status_code=404)
        else:
            deleted_data_produk_group = await delete_data_produk_group(db=db, group_id=group_id, identity=identity)
            result = await show_success(data=deleted_data_produk_group, http_request=http_request, status_code=status.HTTP_200_OK)

        # Return result['status']['code'] akan dikembalikan sesuai yang dikirim diatas,
        return JSONResponse(content=result, status_code=result['status']['code'])
    except Exception as e:
        logging.error(f"Exception delete_produk_group: {e}")
        result = show_bad_response(error=str(e), http_request=http_request)
        return JSONResponse(content=result)
    
# END CODE ROUTE PRODUK GROUP