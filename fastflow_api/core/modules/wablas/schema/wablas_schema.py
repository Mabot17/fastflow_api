# ============================================= Start Noted Schema ===================================
# Author : Abdul Rohman Masrifan | https://fastflow.pybot.cloud/ | masrifan26@gmail.com
# ============================================= END Noted Schema ===================================
from fastapi import UploadFile, Form, File, UploadFile, HTTPException
from database import SessionLocal
from pydantic import BaseModel, Field, field_validator
from typing import Optional, List, Literal, Union
from sqlalchemy.orm import Session
from core.shared.base import (
    DaftarBaseSchema,
    PagingSchema,
    StatusResponseSchema,
    ResponseBaseSchema,
    ErrorSchema,
    RequestSchema
)
from enum import Enum

class WablasSendMessageTextSchema(BaseModel):
    phone: Union[str, int] = Field(default=None, example="087863975153")
    message: str = Field(default=None, example="Tes kirim pesan ERP2 PY.")
    is_group : Optional[bool] = None

ALLOWED_IMAGE_TYPES = {"image/png", "image/jpeg", "image/jpg", "image/gif", "image/bmp"}

class WablasSendMessageImageSchema(BaseModel):
    phone: Union[str, int]
    caption: Optional[str]
    image_file: UploadFile

    @classmethod
    def as_form(
        cls,
        phone: str = Form(...),
        caption: str = Form(...),
        image_file: UploadFile = File(...),
    ):
        return cls(phone=phone, caption=caption, image_file=image_file)

    @field_validator("image_file")
    @classmethod
    def check_image(cls, file: UploadFile):
        if file.content_type not in ALLOWED_IMAGE_TYPES:
            raise HTTPException(status_code=400, detail="Hanya file gambar yang diperbolehkan (PNG, JPG, JPEG, GIF, BMP)")
        return file