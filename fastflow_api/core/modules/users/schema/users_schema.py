# ============================================= Start Noted Schema ===================================
# Author : Abdul Rohman Masrifan | https://fastflow.pybot.cloud/ | masrifan26@gmail.com
# ============================================= END Noted Schema ===================================
from fastapi import Form, Query
from core.config import ZONA_WAKTU_SERVER
from database import SessionLocal
from sqlalchemy.orm import Session
from datetime import date
from pydantic import BaseModel, EmailStr, constr, Field, field_validator
from typing import Optional, List, Literal
from enum import Enum
from core.shared.base import (
    DaftarBaseSchema,
    PagingSchema,
    StatusSchema,
    StatusResponseSchema,
    ResponseBaseSchema,
    JenisKelamin,
    StatusRecord,
    ResponseBaseSchema,
    ErrorSchema,
    RequestSchema
)

class AccountStatusSchema(BaseModel):
    kode: int
    keterangan: str


class UsersBaseSchema(BaseModel):
    user_name: str
    user_kode: str = None
    user_aktif: Literal['Aktif', 'Tidak Aktif'] = 'Aktif'
    user_keterangan: str

    # Validasi panjang maksimal user_kode
    @field_validator('user_kode')
    def validate_user_kode_length(cls, value):
        if value is not None and len(value) > 5:
            raise ValueError("Kode user maksimal 5 karakter.")
        return value

    class Config:
        # orm_mode = False
        from_attributes = False

class IdentitySchema(UsersBaseSchema):
    id: int


class UsersRespBaseSchema(UsersBaseSchema):
    status: Optional[StatusSchema]
    account_status: AccountStatusSchema


class UsersRespSchema(ResponseBaseSchema):
    status: StatusResponseSchema
    data: UsersRespBaseSchema

class UsersSingleSchema(ResponseBaseSchema):
    data: UsersBaseSchema
    error: ErrorSchema
    request: RequestSchema

class UsersRequestListSchema(BaseModel):
    # Inisialisasi obj & set nilai default untuk validasi pydantic
    keywords: Optional[str] = Field(default=None)
    page: int = Field(default=1, gt=0)
    results_per_page: int = Field(default=20, gt=0, le=100)
    timestamp_data: Optional[bool] = Field(default=False)
    user_aktif: Optional[Literal['Aktif', 'Tidak Aktif', 'Semua']] = Query('Semua')

    # as form = membuat sebuah form untuk dokumentasi
    @classmethod
    def as_form(
        cls,
        keywords: str = Query(None),
        page: int = Query(1, gt=0),
        results_per_page: int = Query(20, gt=0, le=100),
        user_aktif: Literal['Aktif', 'Tidak Aktif', 'Semua'] = Query('Semua', description="Status user"),
        timestamp_data: bool = Query(False, description="Jika true, JSON akan disertakan detail timestamp."),
    ):
        return cls(
            keywords=keywords,
            page=page,
            results_per_page=results_per_page,
            timestamp_data=timestamp_data,
            user_aktif=user_aktif,
        )

class UsersReqSchema(UsersBaseSchema):
    # Cara baca property ini adalah : properti di bawah merupakan tambahan dari property di UsersBaseSchema
    password: str
    strict_password: Optional[bool] = False

    @classmethod
    def as_form(
        cls,
        user_name: str = Form(..., description="Username char unik"),
        user_kode: str = Form(..., description="Kode Unik maksimal 2 char", example='RX'),
        password: str = Form(...),
        strict_password: bool = Form(False),
        user_aktif: Literal['Aktif', 'Tidak Aktif'] = Form("Aktif", description="Status user, pilih antara `Aktif` atau `Tidak Aktif`"),
        user_keterangan: str = Form("", description="Keterangan Text Biasa"),
    ):
        return cls(
            user_kode=user_kode,
            user_name=user_name,
            password=password,
            strict_password=strict_password,
            user_aktif=user_aktif,
            user_keterangan=user_keterangan,
        )
    
class UsersPutSchema(UsersBaseSchema):
    user_kode: Optional[str] = Field(default=None)
    user_name: Optional[str] = Field(default=None, example='rohman')
    user_aktif: Optional[Literal['Aktif', 'Tidak Aktif']] = Field(default='Aktif')
    user_keterangan: Optional[str] = Field(default=None)

class UsersPatchSchema(UsersBaseSchema):
    user_kode: Optional[str] = Field(default=None)
    user_name: Optional[str] = Field(default=None, example='rohman')
    user_aktif: Optional[Literal['Aktif', 'Tidak Aktif']] = Field(default='Aktif')
    user_keterangan: Optional[str] = Field(default=None)
    password: Optional[str] = Field(default=None)
    strict_password: Optional[bool] = False

class DaftarUserSchema(DaftarBaseSchema):
    status: StatusResponseSchema
    paging: PagingSchema
    data: List[UsersRespBaseSchema]

class RequestResetPasswordReqSchema(BaseModel):
    username: str
    zona_waktu: Optional[str] = ZONA_WAKTU_SERVER
    show_sms_result: Optional[bool] = False


class UsersGantiEmailReqSchema(BaseModel):
    email_baru: EmailStr
    zona_waktu: Optional[str] = ZONA_WAKTU_SERVER
    show_sms_result: Optional[bool] = False


class UsersValidasiGantiEmailReqSchema(BaseModel):
    email_baru: EmailStr
    otp: str


class UsersGantiHPReqSchema(BaseModel):
    hp_baru: str
    zona_waktu: Optional[str] = ZONA_WAKTU_SERVER
    show_sms_result: Optional[bool] = False


class UsersUpdateNIKReqSchema(BaseModel):
    nik: str

class UrutanDaftarHistoryReferral(Enum):
    TERBARU = "terbaru"
    TERLAMA = "terlama"
    NAMA_DEPAN_TERKECIL = "nama_depan_terkecil"
    NAMA_DEPAN_TERBESAR = "nama_depan_terbesar"
    NAMA_BELAKANG_TERKECIL = "nama_belakang_terkecil"
    NAMA_BELAKANG_TERBESAR = "nama_belakang_terbesar"
    EMAIL_TERKECIL = "email_terkecil"
    EMAIL_TERBESAR = "email_terbesar"
    NO_HP_TERKECIL = "hp_terkecil"
    NO_HP_TERBESAR = "hp_terbesar"
