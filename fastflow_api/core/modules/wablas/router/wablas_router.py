# ============================================= Start Noted Router ===================================
# Author : Abdul Rohman Masrifan | https://fastflow.pybot.cloud/ | masrifan26@gmail.com
# ============================================= END Noted Router ===================================
import requests, httpx
from fastapi import (
    APIRouter,
    HTTPException,
    Header,
    Body,
    Depends,
    status,
    Path,
    Query,
    Request,
    BackgroundTasks
)
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from core.modules.wablas.crud.wablas_crud import (
    send_text_data_wablas,
    send_image_data_wablas
)
from core.modules.users.schema.users_schema import (
    UsersReqSchema,
)
from core.modules.wablas.schema.wablas_schema import (
    WablasSendMessageTextSchema,
    WablasSendMessageImageSchema
)
from core.utils.oauth2 import get_current_user
from core.utils.response_handle import (
    show_success_list,
    show_success,
    show_not_found,
    show_bad_response,
    show_bad_request,
    get_example_responses
)
import logging

# START CODE ROUTE WABLAS
routerWablas = APIRouter(tags=["WABLAS - Tools Pengiriman Whatsapp"], prefix="/wablas")
example_responses = get_example_responses(status_codes=[401, 404, 405, 422, 500])

@routerWablas.post("/send_text")
async def send_message_text(
    http_request: Request,
    request: WablasSendMessageTextSchema,
):
    
    """
        **Catatan attribut param:** 

        - `phone`: [Str] =  single: `087863975153`, jika group phone: `120363046301279079`
        - `message`: [Str] = Tes kirim pesan ERP2 PY.
        - `is_group`: [Bool] = Optional, jika single tidak perlu dikirim paramnya / di false kan
    """

    try:
        data_wablas = await send_text_data_wablas(request=request)

        if data_wablas is not None:
            # Periksa respons
            status_wablas = data_wablas.get("status")
            message_wablas = data_wablas.get("message", "")
            
            if status_wablas:
                data = data_wablas.get("data", {})
                result = await show_success(data=data, message=message_wablas, http_request=http_request, status_code=status.HTTP_200_OK)
            else:
                result = await show_not_found(http_request=http_request, message=message_wablas, status_code=404)
            
            return JSONResponse(content=result, status_code=result['status']['code'])
        else:
            result = show_bad_response(message='WABLAS_TOKEN atau WABLAS_SECRET_KEY tidak boleh kosong!', http_request=http_request, status_code=500)
            return JSONResponse(content=result, status_code=result['status']['code'])
    
    except Exception as e:
        logging.error(f"Exceptioan list_wablas: {e}")
        result = show_bad_response(error=str(e), http_request=http_request)
        return JSONResponse(content=result, status_code=result['status']['code'])
    
@routerWablas.post("/send_image")
async def send_message_image(
    http_request: Request,
    request: WablasSendMessageImageSchema = Depends(WablasSendMessageImageSchema.as_form)
):
    
    """
        **Catatan attribut param:** 

        - `phone`: [Str] = 087863975153
        - `caption`: [Str] = Tes kirim pesan ERP2 PY.
        - `image_file`: [File] = type file
    """

    try:
        data_wablas = await send_image_data_wablas(request=request)
        # return data_wablas

        if data_wablas is not None:
            # Periksa respons
            status_wablas = data_wablas.get("status")
            message_wablas = data_wablas.get("message", "")
            
            if status_wablas:
                data = data_wablas.get("data", {})
                result = await show_success(data=data, message=message_wablas, http_request=http_request, status_code=status.HTTP_200_OK)
            else:
                result = await show_not_found(http_request=http_request, message=message_wablas, status_code=404)
            
            return JSONResponse(content=result, status_code=result['status']['code'])
        else:
            result = show_bad_response(message='WABLAS_TOKEN atau WABLAS_SECRET_KEY tidak boleh kosong!', http_request=http_request, status_code=500)
            return JSONResponse(content=result, status_code=result['status']['code'])
    
    except Exception as e:
        logging.error(f"Exceptioan list_wablas: {e}")
        result = show_bad_response(error=str(e), http_request=http_request)
        return JSONResponse(content=result, status_code=result['status']['code'])