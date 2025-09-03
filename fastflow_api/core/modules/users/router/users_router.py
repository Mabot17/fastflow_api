# ============================================= Start Noted Router ===================================
# Author : Abdul Rohman Masrifan | https://fastflow.pybot.cloud/ | masrifan26@gmail.com
# 1. @routerUsers.get("/daftar", response_model=UsersListSchema) >> routerUsers = abstrack class dari APIRouter. dipanggil di router/api_router.py
# 2. responseHandle = ResponseHandle() >> responseHandle = abstrack class standart dari core/utils/response_handle.py
# 3. async def get_daftar_faktur_pajak() >> Nama function akan dijadikan title di main.py, misal get_daftar_faktur_pajak
# 4. identity: UsersReqSchema = Depends(get_current_user),
#   - async def sample_function(
#       identity: UsersReqSchema = Depends(get_current_user) >> parameter `identity : ` Ini digunakan MENGGUNAKAN / TIDAK TOKEN saat akses api
# 5. Contoh rq ke file crud.py : get_daftar_faktur_pajak && get_crud_daftar_faktur_pajak dibedakan >> supaya memudahkan klik function
# 6. 'http_request: Request` >> menginisialisasikan scarlete.object untuk mengambil request awal dari http
# 7. request: UsersReqSchema = Depends(UsersReqSchema.as_form)
#       - request: UsersReqSchema = Depends(UsersReqSchema.as_form) -> type data form
#       - request: UsersReqSchema = application/json
# ============================================= END Noted Router ===================================
from fastapi import (
    APIRouter,
    Depends,
    Path,
    Query,
    BackgroundTasks,
    status,
    UploadFile,
    File,
    Form,
    Request,
)
from fastapi.responses import JSONResponse
from typing import Optional
from sqlalchemy.orm import Session
from database import get_db
from core.modules.users.schema.users_schema import (
    UsersRequestListSchema,
    DaftarUserSchema,
    UsersRespSchema,
    UsersSingleSchema,
    UsersPatchSchema,
    UsersReqSchema,
    UsersPutSchema,
    UsersBaseSchema,
)
from core.config import ZONA_WAKTU_SERVER, SMS_ENABLED
from core.utils.oauth2 import get_current_user
from core.modules.users.crud.users_crud import (
    get_crud_list_users,
    create_data_user,
    update_data_user,
    delete_data_user,
    select_user_by_id,
    partial_update_data_user,
)
from core.modules.users.model.users_model import (
    UsersModel
)

from core.shared.check_data_model import (
    check_users,
    check_usergroups,
    check_user_by_username,
    check_user_by_kode
)

from core.utils.response_handle import (
    show_success_list,
    show_success,
    show_not_found,
    show_bad_response,
    show_bad_request,
    get_example_responses,
)

import logging

routerUser = APIRouter(tags=["Sistem - Users"], prefix="/users")

# Tambahan contoh request disetiap endpoint, ada di
example_responses = get_example_responses(status_codes=[400, 401, 404, 405, 422, 500])
example_responses_not_auth = get_example_responses(status_codes=[400, 404, 405, 422, 500])

@routerUser.get("/list", response_model=DaftarUserSchema, responses=example_responses)
async def get_all_users(
    http_request: Request,
    request: UsersRequestListSchema = Depends(UsersRequestListSchema.as_form),
    identity: UsersReqSchema = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    try:
        daftar = await get_crud_list_users(db=db, request=request)

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
            result = await show_not_found(http_request=http_request, status_code=404, error="Data User Tidak Ditemukan")

        # Return result['status']['code'] akan dikembalikan sesuai yang dikirim diatas,
        return JSONResponse(content=result, status_code=result['status']['code'])
    except Exception as e:
        logging.error(f"Exception list_users: {e}")
        result = show_bad_response(error=str(e), http_request=http_request)
        return JSONResponse(content=result)

@routerUser.get("/{user_id}", response_model=UsersSingleSchema, responses=example_responses)
async def get_users(
    http_request: Request,
    timestamp_data: bool = Query(False, description="Jika true, JSON akan disertakan detail timestamp."),
    user_id: int = Path(..., description="ID dari API GET `/sistem/users` (get_all_users) -> key `user_id` "),
    db: Session = Depends(get_db),
    data_group_detail: bool = Query(False, description="Jika true, JSON akan disertakan detail group."),
    identity: UsersReqSchema = Depends(get_current_user),
):
    try:
        user_data = await select_user_by_id( db, user_id=user_id, timestamp_data=timestamp_data, data_group_detail=data_group_detail)
        if not user_data:
            result = await show_not_found(http_request=http_request, status_code=404, error="Data User Tidak Ditemukan")
        else:
            result = await show_success(data=user_data, http_request=http_request, status_code=status.HTTP_200_OK)

        # Return result['status']['code'] akan dikembalikan sesuai yang dikirim diatas,
        return JSONResponse(content=result, status_code=result['status']['code'])
    except Exception as e:
        logging.error(f"Exception single_list_users: {e}")
        result = show_bad_response(error=str(e), http_request=http_request)
        return JSONResponse(content=result)


@routerUser.post("", response_model=UsersSingleSchema, responses=example_responses)
async def create_user(
    http_request: Request,
    bt: BackgroundTasks,
    request: UsersReqSchema,
    db: Session = Depends(get_db),
    identity: UsersReqSchema = Depends(get_current_user),
):  
    
    """
    **Catatan:** 
        
    - `user_groups` [Int] dari API `/sistem/usergroups` -> get_all_usergroups key `group_id`\n
    - `user_name` [text] biasa, char unix (tidak boleh sama dengan user_name sebelumnya)\n
    - `user_kode` [text] biasa cth `RM` maksimal 2 char , char unix (tidak boleh sama dengan user_name sebelumnya)\n
    - `user_karyawan` [Int] -> Karyawan ID dari API `/master/karyawan` -> get_all_karyawan key `karyawan_id`  \n
    - `user_aktif_2fa` [Enum], Opsinya `Aktif` atau `Tidak Aktif` -> Dipakai Untuk mengaktifkan/menonaktifkan 2fa pada user terkait\n
    - `user_aktif` [Enum], Opsinya `Aktif` atau `Tidak Aktif`\n -> mengaktifkan/menonaktifkan User
    - `user_password`, sebisa mungkin unik\n
    - `user_keterangan` text biasa\n
    """
    from core.utils.common import validasi_password
    try:
        user = await check_user_by_username(db, user_name=request.user_name)
        if user:
            result = await show_bad_request(http_request=http_request, error="Username sudah terdaftar", status_code=status.HTTP_400_BAD_REQUEST)
            return JSONResponse(content=result, status_code=result['status']['code'])
        
        user_kode = await check_user_by_kode(db, user_kode=request.user_kode)
        if user_kode:
            result = await show_bad_request(http_request=http_request, error=f"User Dengan Kode {request.user_kode} Sudah terdaftar sebelumnya", status_code=status.HTTP_400_BAD_REQUEST)
            return JSONResponse(content=result, status_code=result['status']['code'])
            

        if request.strict_password:
            val_pass = validasi_password(request.password)
            if not val_pass["result"]:
                result = await show_bad_request(http_request=http_request, error=val_pass["message"], status_code=status.HTTP_400_BAD_REQUEST)
                return JSONResponse(content=result, status_code=result['status']['code'])

        new_user = await create_data_user(db=db, user_data_create=request)
        if new_user:
            result = await show_success(data=new_user, http_request=http_request, code_message='createTrue', status_code=status.HTTP_201_CREATED)
        else:
            result = await show_success(http_request=http_request, code_message='createFalse', status_code=status.HTTP_422_UNPROCESSABLE_ENTITY)

        return JSONResponse(content=result, status_code=result['status']['code'])
    except Exception as e:
        logging.error(f"Exception create_users: {e}")
        result = show_bad_response(error=str(e), http_request=http_request)
        return JSONResponse(content=result)


@routerUser.put("/{user_id}", response_model=UsersSingleSchema, responses=example_responses)
async def update_user(
    http_request: Request,
    request: UsersPutSchema,
    user_id: int = Path(..., description="ID dari API GET `/sistem/users` (get_all_users) -> key `user_id` "),
    db: Session = Depends(get_db),
    identity: UsersPutSchema = Depends(get_current_user),
):
    
    """
    **Catatan:** 
        
    - `user_groups` [Int] dari API `/sistem/usergroups` -> get_all_usergroups key `group_id`\n
    - `user_name` [text] biasa, char unix (tidak boleh sama dengan user_name sebelumnya)\n
    - `user_kode` [text] biasa cth `RM` maksimal 2 char , char unix (tidak boleh sama dengan user_name sebelumnya)\n
    - `user_karyawan` [Int] -> Karyawan ID dari API `/master/karyawan` -> get_all_karyawan key `karyawan_id`  \n
    - `user_aktif_2fa` [Enum], Opsinya `Aktif` atau `Tidak Aktif` -> Dipakai Untuk mengaktifkan/menonaktifkan 2fa pada user terkait\n
    - `user_aktif` [Enum], Opsinya `Aktif` atau `Tidak Aktif`\n -> mengaktifkan/menonaktifkan User
    - `user_password`, sebisa mungkin unik\n
    - `user_keterangan` text biasa\n
    """
        
    try:
        user = await check_users(db, user_id=user_id)
        if not user:
            result = await show_not_found(http_request=http_request, error="Data User Tidak Ditemukan", status_code=404)
            return JSONResponse(content=result, status_code=result['status']['code'])

        updated_user = await update_data_user(db=db, user_id=user_id, user_data_update=request, identity=identity)
        if updated_user:
            result = await show_success(data=updated_user, http_request=http_request, code_message='updateTrue', status_code=status.HTTP_200_OK)
        else:
            result = await show_success(http_request=http_request, code_message='updateFalse', status_code=status.HTTP_422_UNPROCESSABLE_ENTITY)

        return JSONResponse(content=result, status_code=result['status']['code'])
    except Exception as e:
        logging.error(f"Exception update_users: {e}")
        result = show_bad_response(error=str(e), http_request=http_request)
        return JSONResponse(content=result)
    
@routerUser.patch("/{user_id}", response_model=UsersSingleSchema, responses=example_responses)
async def partial_update_user(
    http_request: Request,
    request: UsersPatchSchema,
    user_id: int = Path(..., description="ID dari API GET `/sistem/users` (get_all_users) -> key `user_id` "),
    db: Session = Depends(get_db),
    identity: UsersReqSchema = Depends(get_current_user),
):
    
    """
    **Catatan:** 
        
    - `user_groups` [Int] dari API `/sistem/usergroups` -> get_all_usergroups key `group_id`\n
    - `user_name` [text] biasa, char unix (tidak boleh sama dengan user_name sebelumnya)\n
    - `user_kode` [text] biasa cth `RM` maksimal 2 char , char unix (tidak boleh sama dengan user_name sebelumnya)\n
    - `user_karyawan` [Int] -> Karyawan ID dari API `/master/karyawan` -> get_all_karyawan key `karyawan_id`  \n
    - `user_aktif_2fa` [Enum], Opsinya `Aktif` atau `Tidak Aktif` -> Dipakai Untuk mengaktifkan/menonaktifkan 2fa pada user terkait\n
    - `user_aktif` [Enum], Opsinya `Aktif` atau `Tidak Aktif`\n -> mengaktifkan/menonaktifkan User
    - `user_password`, sebisa mungkin unik\n
    - `user_keterangan` text biasa\n
    """
    from core.utils.common import validasi_password

    try:
        user = await check_users(db, user_id=user_id)
        if not user:
            result = await show_not_found(http_request=http_request, error="Data User Tidak Ditemukan", status_code=404)
            return JSONResponse(content=result, status_code=result['status']['code'])

        if request.strict_password:
            val_pass = validasi_password(request.password)
            if not val_pass["result"]:
                result = await show_bad_request(http_request=http_request, error=val_pass["message"], status_code=status.HTTP_400_BAD_REQUEST)
                return JSONResponse(content=result, status_code=result['status']['code'])

        updated_user = await partial_update_data_user(db=db, user_id=user_id, user_data_update=request.dict(exclude_unset=True), identity=identity)
        if updated_user:
            result = await show_success(data=updated_user, http_request=http_request, code_message='updateTrue', status_code=status.HTTP_200_OK)
        else:
            result = await show_success(http_request=http_request, code_message='updateFalse', status_code=status.HTTP_422_UNPROCESSABLE_ENTITY)

        return JSONResponse(content=result, status_code=result['status']['code'])
    except Exception as e:
        logging.error(f"Exception update_patch_users: {e}")
        result = show_bad_response(error=str(e), http_request=http_request)
        return JSONResponse(content=result)

@routerUser.delete("/{user_id}", response_model=UsersRespSchema, include_in_schema=True)
async def delete_user(
    http_request: Request,
    user_id: int,
    db: Session = Depends(get_db),
    identity: UsersReqSchema = Depends(get_current_user),
):
    try:
        user = await check_users(db, user_id=user_id)
        if not user:
            result = await show_not_found(http_request=http_request, error="Data User Tidak Ditemukan", status_code=404)
        else:
            deleted_user = await delete_data_user(db, user_id=user_id, identity=identity)
            if deleted_user:
                result = await show_success(data=deleted_user, http_request=http_request, code_message='deleteTrue', status_code=status.HTTP_200_OK)
            else:
                result = show_bad_response(error='Data user gagal dihapus')

        # Return result['status']['code'] akan dikembalikan sesuai yang dikirim diatas,
        return JSONResponse(content=result, status_code=result['status']['code'])
    except Exception as e:
        logging.error(f"Exception delete_users: {e}")
        result = show_bad_response(error=str(e), http_request=http_request)
        return JSONResponse(content=result)