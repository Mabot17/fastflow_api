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

class TextToVoiceSendMessageTextSchema(BaseModel):
    text: str = Field(default=None, example="Halo Selamat Datang, di dunia modern digital.")