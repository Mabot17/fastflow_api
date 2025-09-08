# ============================================= Start Noted Router ===================================
# Author : PT. Dapur Perangkat Lunak Indonesia | KoffieSoft Group | https://www.koffiesoft.com/ | info@koffiesoft.com
# 1. @routerSatuan.get("/daftar", response_model=SatuanListSchema) >> routerSatuan = abstrack class dari APIRouter. dipanggil di router/api_router.py
# 2. responseHandle = ResponseHandle() >> responseHandle = abstrack class standart dari core/utils/response_handle.py
# 3. async def get_daftar_satuan() >> Nama function akan dijadikan title di main.py, misal get_daftar_satuan
# 4. identity: UsersReqSchema = Depends(get_current_user),
#   - async def sample_function(
#       identity: UsersReqSchema = Depends(get_current_user) >> parameter `identity : ` Ini digunakan MENGGUNAKAN / TIDAK TOKEN saat akses api
# 5. Contoh rq ke file crud.py : get_daftar_satuan && get_crud_daftar_satuan dibedakan >> supaya memudahkan klik function
# 6. 'http_request: Request` >> menginisialisasikan scarlete.object untuk mengambil request awal dari http
# 7. request: SatuanReqSchema = Depends(SatuanReqSchema.as_form)
#       - request: SatuanReqSchema = Depends(SatuanReqSchema.as_form) -> type data form
#       - request: SatuanReqSchema = application/json
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
from core.modules.satuan.crud.satuan_crud import (
    get_crud_daftar_satuan,
    select_satuan_by_id,
    create_data_satuan,
    update_data_satuan,
    partial_update_data_satuan,
    delete_data_satuan
)
from core.modules.users.schema.users_schema import (
    UsersReqSchema,
)
from core.modules.satuan.schema.satuan_schema import (
    SatuanBaseDataSchema,
    SatuanRequestListSchema,
    SatuanListSchema,
    SatuanReqSchema,
    SatuanPutSchema,
    SatuanPatchSchema,
    SatuanSingleSchema
)
from core.utils.oauth2 import get_current_user
from core.shared.check_data_model import (
    check_satuan,
    check_satuan_kode
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

# START CODE ROUTE JABATAN
routerSatuan = APIRouter(tags=["Master - Satuan"], prefix="/satuan")

example_responses = get_example_responses(status_codes=[401, 404, 405, 422, 500])

# ROUTE LIST & SEARCH DATA JABATAN
@routerSatuan.get("", response_model=SatuanListSchema, responses=example_responses)
async def get_all_satuan(
    http_request: Request,
    request: SatuanRequestListSchema = Depends(SatuanRequestListSchema.as_form),
    identity: UsersReqSchema = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    try:
        daftar = await get_crud_daftar_satuan(db=db, request=request)

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
        logging.error(f"Exception list_satuan: {e}")
        result = show_bad_response(error=str(e), http_request=http_request)
        return JSONResponse(content=result)

# ROUTE GET DATA JABATAN BY ID
@routerSatuan.get("/{satuan_id}", response_model=SatuanSingleSchema, responses=example_responses)
async def get_satuan(
    http_request: Request,
    timestamp_data: bool = Query(False, description="Jika true, JSON akan disertakan detail timestamp."),
    satuan_id: int = Path(..., description="ID dari API GET `/master/satuan` (get_all_satuan) -> key `satuan_id` "),
    db: Session = Depends(get_db),
    identity: UsersReqSchema = Depends(get_current_user),
):
    try:
        data_satuan = await select_satuan_by_id(db, satuan_id=satuan_id, timestamp_data=timestamp_data)
        if not data_satuan:
            result = await show_not_found(http_request=http_request, status_code=404)
        else:
            result = await show_success(data=data_satuan, http_request=http_request, status_code=status.HTTP_200_OK)

        # Return result['status']['code'] akan dikembalikan sesuai yang dikirim diatas,
        return JSONResponse(content=result, status_code=result['status']['code'])
    except Exception as e:
        logging.error(f"Exception single_list_satuan: {e}")
        result = show_bad_response(error=str(e), http_request=http_request)
        return JSONResponse(content=result)

# ROUTE CREATE DATA JABATAN
@routerSatuan.post("", response_model=SatuanSingleSchema, responses=example_responses)
async def create_satuan(
    http_request: Request,
    bt: BackgroundTasks,
    request: SatuanReqSchema,
    db: Session = Depends(get_db),
    identity: UsersReqSchema = Depends(get_current_user),
):
    
    """
        **Catatan:** 

        `satuan_aktif`: ENUM pilihan `Aktif`/`Tidak Aktif` \n
    """

        
    try:
        if request.satuan_kode is not None:
            satuan_check = await check_satuan_kode(db, satuan_kode=request.satuan_kode)
            if satuan_check:
                result = await show_bad_request(http_request=http_request, error=f"Kode Satuan {request.satuan_kode} Sudah terdaftar sebelumnya", status_code=status.HTTP_400_BAD_REQUEST)
                return JSONResponse(content=result, status_code=result['status']['code'])
            
        new_satuan = await create_data_satuan(db=db, satuan_data_create=request, identity=identity)
        if new_satuan:
            result = await show_success(data=new_satuan, http_request=http_request, code_message='createTrue', status_code=status.HTTP_201_CREATED)
        else:
            result = await show_success(http_request=http_request, code_message='createFalse', status_code=status.HTTP_422_UNPROCESSABLE_ENTITY)
            
        return JSONResponse(content=result, status_code=result['status']['code'])
    except Exception as e:
        logging.error(f"Exception create_satuan: {e}")
        result = show_bad_response(error=str(e), http_request=http_request)
        return JSONResponse(content=result, status_code=result['status']['code'])

# ROUTE UPDATE DATA JABATAN
@routerSatuan.put("/{satuan_id}", response_model=SatuanSingleSchema, responses=example_responses)
async def update_satuan(
    http_request: Request,
    request: SatuanPutSchema,
    satuan_id: int = Path(..., description="ID dari API GET `/master/satuan` (get_all_satuan) -> key `satuan_id` "),
    db: Session = Depends(get_db),
    identity: UsersReqSchema = Depends(get_current_user),
):
    
    """
        **Catatan:** 

        `satuan_aktif`: ENUM pilihan `Aktif`/`Tidak Aktif` \n
    """
        
    try:
        if request.satuan_kode is not None:
            satuan_check = await check_satuan_kode(db, satuan_kode=request.satuan_kode, exclude_satuan_id=satuan_id)
            if satuan_check:
                result = await show_bad_request(http_request=http_request, error=f"Kode Satuan {request.satuan_kode} Sudah terdaftar sebelumnya", status_code=status.HTTP_400_BAD_REQUEST)
                return JSONResponse(content=result, status_code=result['status']['code'])
    
        check_data_satuan = await check_satuan(db, satuan_id=satuan_id)
        if not check_data_satuan:
            result = await show_not_found(http_request=http_request, status_code=404)
        else:
            data_satuan = await update_data_satuan(db=db, satuan_id=satuan_id, satuan_data_update=request, identity=identity)
            result = await show_success(data=data_satuan, http_request=http_request, status_code=status.HTTP_200_OK)

        # Return result['status']['code'] akan dikembalikan sesuai yang dikirim diatas,
        return JSONResponse(content=result, status_code=result['status']['code'])
    except Exception as e:
        logging.error(f"Exception update_satuan: {e}")
        result = show_bad_response(error=str(e), http_request=http_request)
        return JSONResponse(content=result)
    
# ROUTE UPDATE PATCH DATA JABATAN
@routerSatuan.patch("/{satuan_id}", response_model=SatuanSingleSchema, responses=example_responses)
async def partial_update_satuan(
    http_request: Request,
    request: SatuanPatchSchema,
    satuan_id: int = Path(..., description="ID dari API GET `/master/satuan` (get_all_satuan) -> key `satuan_id` "),
    db: Session = Depends(get_db),
    identity: UsersReqSchema = Depends(get_current_user),
):
    
    """
        **Catatan:** 

        `satuan_aktif`: ENUM pilihan `Aktif`/`Tidak Aktif` \n
    """
        
    try:
        check_data_satuan = await check_satuan(db, satuan_id=satuan_id)
        if not check_data_satuan:
            result = await show_not_found(http_request=http_request, status_code=404)
        else:
            data_satuan = await partial_update_data_satuan(db=db, satuan_id=satuan_id, satuan_data_update=request.dict(exclude_unset=True), identity=identity)
            result = await show_success(data=data_satuan, http_request=http_request, status_code=status.HTTP_200_OK)

        # Return result['status']['code'] akan dikembalikan sesuai yang dikirim diatas,
        return JSONResponse(content=result, status_code=result['status']['code'])
    except Exception as e:
        logging.error(f"Exception update_patch_satuan: {e}")
        result = show_bad_response(error=str(e), http_request=http_request)
        return JSONResponse(content=result)

# ROUTE DELETE DATA JABATAN
@routerSatuan.delete("/{satuan_id}", response_model=SatuanSingleSchema, responses=example_responses)
async def delete_satuan(
    http_request: Request,
    satuan_id: int = Path(..., description="ID dari API GET `/master/satuan` (get_all_satuan) -> key `satuan_id` "),
    db: Session = Depends(get_db),
    identity: UsersReqSchema = Depends(get_current_user),
):
    try:
        check_data_satuan = await check_satuan(db, satuan_id=satuan_id)
        if not check_data_satuan:
            result = await show_not_found(http_request=http_request, status_code=404)
        else:
            deleted_data_satuan = await delete_data_satuan(db=db, satuan_id=satuan_id, identity=identity)
            result = await show_success(data=deleted_data_satuan, http_request=http_request, status_code=status.HTTP_200_OK)

        # Return result['status']['code'] akan dikembalikan sesuai yang dikirim diatas,
        return JSONResponse(content=result, status_code=result['status']['code'])
    except Exception as e:
        logging.error(f"Exception delete_satuan: {e}")
        result = show_bad_response(error=str(e), http_request=http_request)
        return JSONResponse(content=result)
    
# END CODE ROUTE JABATAN