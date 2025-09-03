# ============================================= Start Noted API Middleware ===================================
# Author : Abdul Rohman Masrifan | https://fastflow.pybot.cloud/ | masrifan26@gmail.com
# 1. @routerLogin.get("/login") >> routerLogin = class dari APIRouter. dipanggil di router/api_router.py
# 2. responseHandle = standart dari core/response_handle.py
# ============================================= END Noted Middleware ===================================
import logging, re
from core.utils.common import SUCCESS, FAILED
from core.utils.hashing import Hash
from core.utils.token import create_access_token

from fastapi import APIRouter, Depends, Header, status, BackgroundTasks
from fastapi.responses import JSONResponse
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from database import get_db
from typing import Optional
from ua_parser import user_agent_parser as uap
from core.modules.auth.schema.login import LoginRespSchema
from core.shared.json_helpers.json_user import json_user

from core.modules.users.schema.users_schema import (
    UsersSingleSchema,
    UsersReqSchema,
)
from core.utils.oauth2 import get_current_user

from core.shared.check_data_model import (
    check_users,
    check_user_by_username
)

from core.utils.response_handle import (
    show_success_list,
    show_success,
    show_not_found,
    show_bad_request,
    show_bad_response,
    show_forbidden_response,
    get_example_responses
)
routerLogin = APIRouter(tags=["Authentication"])


@routerLogin.post("/login", response_model=LoginRespSchema)
async def login(
    bt: BackgroundTasks,
    user_agent: Optional[str] = Header(None),
    db: Session = Depends(get_db),
    request: OAuth2PasswordRequestForm = Depends(),
):
    logging.debug(f"login: {request.scopes}")

    if user_agent:
        ua_dict = uap.Parse(user_agent)
        logging.debug(ua_dict)

    user = await check_user_by_username(db, user_name=request.username)
    if not user:
        result = await show_not_found(error="Username belum terdaftar", status_code=status.HTTP_404_NOT_FOUND)
        return JSONResponse(content=result, status_code=result['status']['code'])
        
    if Hash.verify(hashed_password=user.user_password, plain_password=request.password):

        data_user = await check_users(db, user_id=user.user_id)
        result_user = await json_user(db=db, user_data_row=data_user, user_karyawan_data=True)

        # Jika OTP tidak aktif, akan langsung dikembalikan token, jika aktif perlu verifikasi dahulu
        # Generate key unix, ini JSON bisa bebas. tapi wajib cocok dengan fungsi verify_token()
        access_token = create_access_token(
            data={
                "sub"       : user.user_name,
                "user_id"   : user.user_id,
                "user_name" : user.user_name,
            }
        )

        if access_token:
            data_user.api_token = access_token
            db.commit()
            db.refresh(data_user)

        content = {
            "status": {"code": 200, "message": SUCCESS},
            "access_token": access_token,
            "token_type": "bearer",
            "data": result_user,
        }
        return JSONResponse(content=content)
    else:
        result = await show_forbidden_response(error="Username atau Password tidak sesuai", status_code=status.HTTP_403_FORBIDDEN)
        return JSONResponse(content=result, status_code=result['status']['code'])

@routerLogin.get("/me", response_model=UsersSingleSchema)
async def get_me(
    db: Session = Depends(get_db),
    identity: UsersReqSchema = Depends(get_current_user),
):
    if identity:
        user_name = identity.user_name
        user_data = await check_user_by_username(db, user_name=user_name)

        if not user_data:
            result = await show_not_found(error="User tidak ditemukan", status_code=status.HTTP_404_NOT_FOUND)
            return JSONResponse(content=result, status_code=result['status']['code'])

        # Konversi data user ke format JSON
        result_user = await json_user(db=db, user_data_row=user_data, data_group_detail=True, user_karyawan_data=True)

        # Kembalikan response dengan data user
        content = {
            "status": {"code": 200, "message": SUCCESS},
            "data": result_user,
        }
        return JSONResponse(content=content, status_code=status.HTTP_200_OK)
    else:
        result = show_bad_response(error="Akun Tidak Terdaftar")
        return JSONResponse(content=result)