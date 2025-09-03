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
import os
from fastapi.responses import FileResponse, JSONResponse
from sqlalchemy.orm import Session
from core.modules.text_to_voice.crud.text_to_voice_crud import (
    text_to_mp3
)
from core.modules.users.schema.users_schema import (
    UsersReqSchema,
)
from core.modules.text_to_voice.schema.text_to_voice_schema import (
    TextToVoiceSendMessageTextSchema,
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

# START CODE ROUTE TEXT TO VOICE
routerTextToVoice = APIRouter(tags=["Text To Voice"], prefix="/text_to_voice")
example_responses = get_example_responses(status_codes=[401, 404, 405, 422, 500])

@routerTextToVoice.post("")
async def generate_voice(
    http_request: Request,
    request: TextToVoiceSendMessageTextSchema,
):
    """
    Kirim teks dan dapatkan file suara (MP3) sebagai respon langsung.
    """
    try:
        mp3_file = text_to_mp3(request.text)
        return FileResponse(
            path=mp3_file,
            media_type="audio/mpeg",
            filename=os.path.basename(mp3_file)
        )
    
    except Exception as e:
        logging.error(f"Exception in send_message_text: {e}")
        return JSONResponse(
            content={"success": False, "error": str(e)},
            status_code=500
        )