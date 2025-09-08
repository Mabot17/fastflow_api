# ============================================= Start Noted Router ===================================
# Author : PT. Dapur Perangkat Lunak Indonesia | KoffieSoft Group | https://www.koffiesoft.com/ | info@koffiesoft.com
# 1. @routerCustomer.get("/daftar", response_model=CustomerListSchema) >> routerCustomer = abstrack class dari APIRouter. dipanggil di router/api_router.py
# 2. responseHandle = ResponseHandle() >> responseHandle = abstrack class standart dari core/utils/response_handle.py
# 3. async def get_daftar_customer() >> Nama function akan dijadikan title di main.py, misal get_daftar_customer
# 4. identity: UsersReqSchema = Depends(get_current_user),
#   - async def sample_function(
#       identity: UsersReqSchema = Depends(get_current_user) >> parameter `identity : ` Ini digunakan MENGGUNAKAN / TIDAK TOKEN saat akses api
# 5. Contoh rq ke file crud.py : get_daftar_customer && get_crud_daftar_customer dibedakan >> supaya memudahkan klik function
# 6. 'http_request: Request` >> menginisialisasikan scarlete.object untuk mengambil request awal dari http
# 7. request: CustomerReqSchema = Depends(CustomerReqSchema.as_form)
#       - request: CustomerReqSchema = Depends(CustomerReqSchema.as_form) -> type data form
#       - request: CustomerReqSchema = application/json
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
from core.modules.customer.crud.customer_crud import (
    get_crud_daftar_customer,
    select_customer_by_id,
    create_data_customer,
    update_data_customer,
    partial_update_data_customer,
    delete_data_customer
)
from core.modules.users.schema.users_schema import (
    UsersReqSchema,
)
from core.modules.customer.schema.customer_schema import (
    CustomerBaseDataSchema,
    CustomerRequestListSchema,
    CustomerListSchema,
    CustomerReqSchema,
    CustomerPutSchema,
    CustomerPatchSchema,
    CustomerSingleSchema
)
from core.utils.oauth2 import get_current_user
from core.shared.check_data_model import (
    check_customer,
    check_cust_no,
    check_cust_nama_lengkap
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

# START CODE ROUTE Customer
routerCustomer = APIRouter(tags=["Master - Customer"], prefix="/customer")

example_responses = get_example_responses(status_codes=[401, 404, 405, 422, 500])

# ROUTE LIST & SEARCH DATA Customer
@routerCustomer.get("", response_model=CustomerListSchema, responses=example_responses)
async def get_all_customer(
    http_request: Request,
    request: CustomerRequestListSchema = Depends(CustomerRequestListSchema.as_form),
    identity: UsersReqSchema = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    try:
        daftar = await get_crud_daftar_customer(db=db, request=request)

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
        logging.error(f"Exception list_customer: {e}")
        result = show_bad_response(error=str(e), http_request=http_request)
        return JSONResponse(content=result)

# ROUTE GET DATA Customer BY ID
@routerCustomer.get("/{cust_id}", response_model=CustomerSingleSchema, responses=example_responses)
async def get_customer(
    http_request: Request,
    timestamp_data: bool = Query(False, description="Jika true, JSON akan disertakan detail timestamp."),
    cust_id: int = Path(..., description="ID dari API GET `/master/customer` (get_all_customer) -> key `cust_id` "),
    db: Session = Depends(get_db),
    identity: UsersReqSchema = Depends(get_current_user),
):
    try:
        data_customer = await select_customer_by_id(db, cust_id=cust_id, timestamp_data=timestamp_data)
        if not data_customer:
            result = await show_not_found(http_request=http_request, status_code=404)
        else:
            result = await show_success(data=data_customer, http_request=http_request, status_code=status.HTTP_200_OK)

        # Return result['status']['code'] akan dikembalikan sesuai yang dikirim diatas,
        return JSONResponse(content=result, status_code=result['status']['code'])
    except Exception as e:
        logging.error(f"Exception single_list_customer: {e}")
        result = show_bad_response(error=str(e), http_request=http_request)
        return JSONResponse(content=result)

# ROUTE CREATE DATA Customer
@routerCustomer.post("", response_model=CustomerSingleSchema, responses=example_responses)
async def create_customer(
    http_request: Request,
    bt: BackgroundTasks,
    request: CustomerReqSchema,
    db: Session = Depends(get_db),
    identity: UsersReqSchema = Depends(get_current_user),
):
    
    """
        **Catatan:**

        - `cust_no` : kode pelanggan, maksimal 10 karakter (**wajib**)   \n
        - `cust_nama_lengkap` : nama lengkap pelanggan, minimal 1 karakter (**wajib**)   \n
        - `cust_nama_panggilan` : nama panggilan, opsional   \n
        - `cust_kelamin` : jenis kelamin, enum **L** (Laki-laki) atau **P** (Perempuan)   \n
        - `cust_alamat` : alamat pelanggan, maksimal 250 karakter (opsional)   \n
        - `cust_hp` : nomor handphone, maksimal 25 karakter (opsional)   \n
        - `cust_aktif` : status pelanggan, enum **Aktif** / **Tidak Aktif** (default: Aktif)   \n
        - `cust_keterangan` : keterangan tambahan, maksimal 1000 karakter (opsional)   \n
    """
        
    try:
        if request.cust_no is not None:
            customer_check = await check_cust_no(db, cust_no=request.cust_no)
            if customer_check:
                result = await show_bad_request(http_request=http_request, error=f"Kode Customer {request.cust_no} Sudah terdaftar sebelumnya", status_code=status.HTTP_400_BAD_REQUEST)
                return JSONResponse(content=result, status_code=result['status']['code'])
            
        if request.cust_nama_lengkap is not None:
            customer_check_nama = await check_cust_nama_lengkap(db, cust_nama_lengkap=request.cust_nama_lengkap)
            if customer_check_nama:
                result = await show_bad_request(http_request=http_request, error=f"Nama Customer {request.cust_nama_lengkap} Sudah terdaftar sebelumnya", status_code=status.HTTP_400_BAD_REQUEST)
                return JSONResponse(content=result, status_code=result['status']['code'])
            
        new_customer = await create_data_customer(db=db, customer_data_create=request, identity=identity)
        if new_customer:
            result = await show_success(data=new_customer, http_request=http_request, code_message='createTrue', status_code=status.HTTP_201_CREATED)
        else:
            result = await show_success(http_request=http_request, code_message='createFalse', status_code=status.HTTP_422_UNPROCESSABLE_ENTITY)
            
        return JSONResponse(content=result, status_code=result['status']['code'])
    except Exception as e:
        logging.error(f"Exception create_customer: {e}")
        result = show_bad_response(error=str(e), http_request=http_request)
        return JSONResponse(content=result, status_code=result['status']['code'])

# ROUTE UPDATE DATA Customer
@routerCustomer.put("/{cust_id}", response_model=CustomerSingleSchema, responses=example_responses)
async def update_customer(
    http_request: Request,
    request: CustomerPutSchema,
    cust_id: int = Path(..., description="ID dari API GET `/master/customer` (get_all_customer) -> key `cust_id` "),
    db: Session = Depends(get_db),
    identity: UsersReqSchema = Depends(get_current_user),
):
    
    """
        **Catatan:**

        - `cust_no` : kode pelanggan, maksimal 10 karakter (**wajib**)   \n
        - `cust_nama_lengkap` : nama lengkap pelanggan, minimal 1 karakter (**wajib**)   \n
        - `cust_nama_panggilan` : nama panggilan, opsional   \n
        - `cust_kelamin` : jenis kelamin, enum **L** (Laki-laki) atau **P** (Perempuan)   \n
        - `cust_alamat` : alamat pelanggan, maksimal 250 karakter (opsional)   \n
        - `cust_hp` : nomor handphone, maksimal 25 karakter (opsional)   \n
        - `cust_aktif` : status pelanggan, enum **Aktif** / **Tidak Aktif** (default: Aktif)   \n
        - `cust_keterangan` : keterangan tambahan, maksimal 1000 karakter (opsional)   \n
    """
        
    try:
        if request.cust_no is not None:
            customer_check = await check_cust_no(db, cust_no=request.cust_no, exclude_cust_id=cust_id)
            if customer_check:
                result = await show_bad_request(http_request=http_request, error=f"Kode Customer {request.cust_no} Sudah terdaftar sebelumnya", status_code=status.HTTP_400_BAD_REQUEST)
                return JSONResponse(content=result, status_code=result['status']['code'])
            
        if request.cust_nama_lengkap is not None:
            customer_check_nama = await check_cust_nama_lengkap(db, cust_nama_lengkap=request.cust_nama_lengkap, exclude_cust_id=cust_id)
            if customer_check_nama:
                result = await show_bad_request(http_request=http_request, error=f"Nama Customer {request.cust_nama_lengkap} Sudah terdaftar sebelumnya", status_code=status.HTTP_400_BAD_REQUEST)
                return JSONResponse(content=result, status_code=result['status']['code'])
    
        check_data_customer = await check_customer(db, cust_id=cust_id)
        if not check_data_customer:
            result = await show_not_found(http_request=http_request, status_code=404)
        else:
            data_customer = await update_data_customer(db=db, cust_id=cust_id, customer_data_update=request, identity=identity)
            result = await show_success(data=data_customer, http_request=http_request, status_code=status.HTTP_200_OK)

        # Return result['status']['code'] akan dikembalikan sesuai yang dikirim diatas,
        return JSONResponse(content=result, status_code=result['status']['code'])
    except Exception as e:
        logging.error(f"Exception update_customer: {e}")
        result = show_bad_response(error=str(e), http_request=http_request)
        return JSONResponse(content=result)
    
# ROUTE UPDATE PATCH DATA Customer
@routerCustomer.patch("/{cust_id}", response_model=CustomerSingleSchema, responses=example_responses)
async def partial_update_customer(
    http_request: Request,
    request: CustomerPatchSchema,
    cust_id: int = Path(..., description="ID dari API GET `/master/customer` (get_all_customer) -> key `cust_id` "),
    db: Session = Depends(get_db),
    identity: UsersReqSchema = Depends(get_current_user),
):
    
    """
        **Catatan:**

        - `cust_no` : kode pelanggan, maksimal 10 karakter (**wajib**)   \n
        - `cust_nama_lengkap` : nama lengkap pelanggan, minimal 1 karakter (**wajib**)   \n
        - `cust_nama_panggilan` : nama panggilan, opsional   \n
        - `cust_kelamin` : jenis kelamin, enum **L** (Laki-laki) atau **P** (Perempuan)   \n
        - `cust_alamat` : alamat pelanggan, maksimal 250 karakter (opsional)   \n
        - `cust_hp` : nomor handphone, maksimal 25 karakter (opsional)   \n
        - `cust_aktif` : status pelanggan, enum **Aktif** / **Tidak Aktif** (default: Aktif)   \n
        - `cust_keterangan` : keterangan tambahan, maksimal 1000 karakter (opsional)   \n
    """
        
    try:
        if request.cust_no is not None:
            customer_check = await check_cust_no(db, cust_no=request.cust_no, exclude_cust_id=cust_id)
            if customer_check:
                result = await show_bad_request(http_request=http_request, error=f"Kode Customer {request.cust_no} Sudah terdaftar sebelumnya", status_code=status.HTTP_400_BAD_REQUEST)
                return JSONResponse(content=result, status_code=result['status']['code'])
            
        if request.cust_nama_lengkap is not None:
            customer_check_nama = await check_cust_nama_lengkap(db, cust_nama_lengkap=request.cust_nama_lengkap, exclude_cust_id=cust_id)
            if customer_check_nama:
                result = await show_bad_request(http_request=http_request, error=f"Nama Customer {request.cust_nama_lengkap} Sudah terdaftar sebelumnya", status_code=status.HTTP_400_BAD_REQUEST)
                return JSONResponse(content=result, status_code=result['status']['code'])
            
        check_data_customer = await check_customer(db, cust_id=cust_id)
        if not check_data_customer:
            result = await show_not_found(http_request=http_request, status_code=404)
        else:
            data_customer = await partial_update_data_customer(db=db, cust_id=cust_id, customer_data_update=request.dict(exclude_unset=True), identity=identity)
            result = await show_success(data=data_customer, http_request=http_request, status_code=status.HTTP_200_OK)

        # Return result['status']['code'] akan dikembalikan sesuai yang dikirim diatas,
        return JSONResponse(content=result, status_code=result['status']['code'])
    except Exception as e:
        logging.error(f"Exception update_patch_customer: {e}")
        result = show_bad_response(error=str(e), http_request=http_request)
        return JSONResponse(content=result)

# ROUTE DELETE DATA Customer
@routerCustomer.delete("/{cust_id}", response_model=CustomerSingleSchema, responses=example_responses)
async def delete_customer(
    http_request: Request,
    cust_id: int = Path(..., description="ID dari API GET `/master/customer` (get_all_customer) -> key `cust_id` "),
    db: Session = Depends(get_db),
    identity: UsersReqSchema = Depends(get_current_user),
):
    try:
        check_data_customer = await check_customer(db, cust_id=cust_id)
        if not check_data_customer:
            result = await show_not_found(http_request=http_request, status_code=404)
        else:
            deleted_data_customer = await delete_data_customer(db=db, cust_id=cust_id, identity=identity)
            result = await show_success(data=deleted_data_customer, http_request=http_request, status_code=status.HTTP_200_OK)

        # Return result['status']['code'] akan dikembalikan sesuai yang dikirim diatas,
        return JSONResponse(content=result, status_code=result['status']['code'])
    except Exception as e:
        logging.error(f"Exception delete_customer: {e}")
        result = show_bad_response(error=str(e), http_request=http_request)
        return JSONResponse(content=result)
    
# END CODE ROUTE Customer