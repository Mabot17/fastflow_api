# ============================================= Start Noted Router ===================================
# Author : Abdul Rohman Masrifan | https://fastflow.pybot.cloud/ | masrifan26@gmail.com
# 1. Response return wajib JSON/dict supaya bisa diolah kembali di router
# ============================================= END Noted Router ===================================
import requests, httpx
from sqlalchemy.orm import Session, aliased
from sqlalchemy import and_, func, or_
from sqlalchemy.exc import IntegrityError
from core.utils.wablas.wablas_storage import ApiWablasStorage
from core.modules.wablas.schema.wablas_schema import (
    WablasSendMessageTextSchema,
    WablasSendMessageImageSchema
)
from core.modules.users.schema.users_schema import UsersBaseSchema
from datetime import datetime
from typing import List, Optional, Dict
from core.utils.upload_foto import upload_image_file, upload_aws_image_file

import logging

async def send_text_data_wablas(request: WablasSendMessageTextSchema,) -> List:
    try:
        base_url = ApiWablasStorage.WABLAS_URL.value
        auth_key = ApiWablasStorage.get_auth_key()
        
        if auth_key is None:
            return None
        
        if request.is_group:
            custom_json = {
                "phone": request.phone,
                "message": request.message,
                "isGroup" : "true"
            }
        else:
            custom_json = {
                "phone": request.phone,
                "message": request.message
            }
        
        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{base_url}/send-message",
                headers={"Authorization": f"{auth_key}"},
                json=custom_json
            )

        print(response.json())
        
        if response:
            return response.json()
        else:
            return None
    
    except IntegrityError as e:
        logging.error(f"IntegrityError: {e}")
        return {"data": None, "total_data" : 0}
    except Exception as e:
        logging.error(e)
        return {"data": None, "total_data" : 0}
    
async def send_image_data_wablas(request: WablasSendMessageImageSchema,) -> List:
    try:
        base_url = ApiWablasStorage.WABLAS_URL.value
        auth_key = ApiWablasStorage.get_auth_key()
        
        if auth_key is None:
            return None
        
        # Upload file AWS
        data_foto = await upload_aws_image_file(
            index=1,
            image_file=request.image_file,
            modul='wablas_file'
        )

        custom_json = {
            "phone": request.phone,
            "caption": request.caption,
            "image": data_foto['fullpath'] 
        }

        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{base_url}/send-image",
                headers={"Authorization": f"{auth_key}"},
                json=custom_json
            )

        if response:
            return response.json()
        else:
            return None
    
    except IntegrityError as e:
        logging.error(f"IntegrityError: {e}")
        return {"data": None, "total_data" : 0}
    except Exception as e:
        logging.error(e)
        return {"data": None, "total_data" : 0}