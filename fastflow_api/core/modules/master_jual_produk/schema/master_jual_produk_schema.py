# ============================================= Start Noted Schema ===================================
# Author : PT. Dapur Perangkat Lunak Indonesia | KoffieSoft Group | https://www.koffiesoft.com/ | info@koffiesoft.com
# ============================================= END Noted Schema ===================================
from datetime import date, datetime
from fastapi import Form, Query, UploadFile, File
from database import SessionLocal
from pydantic import BaseModel, Field, field_validator
from typing import Optional, List, Literal
from sqlalchemy.orm import Session
from core.shared.base import (
    DaftarBaseSchema,
    PagingSchema,
    StatusResponseSchema,
    ResponseBaseSchema,
    ErrorSchema,
    RequestSchema
)
from core.shared.base_validation_model_schema import validate_customer_by_id

class MasterJualProdukBaseDataSchema(BaseModel):
    jproduk_tanggal: date = None
    jproduk_cust: int
    jproduk_diskon: float = None
    jproduk_cara: Literal['tunai','card','transfer'] = 'tunai'
    jproduk_keterangan: str = None
    jproduk_stat_dok: Literal['Terbuka','Tertutup','Batal','Tunggu','Sementara'] = 'Terbuka'
    jproduk_bayar: float = None
    jproduk_totalbiaya: float = None

    # Field validator untuk memvalidasi jproduk_cust
    @field_validator('jproduk_cust')
    def validate_customer(cls, value):
        if value is not None:
            validate_customer_by_id(value)
        return value


class MasterJualProdukListSchema(ResponseBaseSchema):
    data: List[MasterJualProdukBaseDataSchema]
    paging: List[PagingSchema]
    error: ErrorSchema
    request: RequestSchema


class MasterJualProdukSingleSchema(ResponseBaseSchema):
    data: MasterJualProdukBaseDataSchema
    error: ErrorSchema
    request: RequestSchema


class MasterJualProdukRequestListSchema(BaseModel):
    keywords: Optional[str] = Field(default=None)
    page: int = Field(default=1, gt=0)
    results_per_page: int = Field(default=20, gt=0, le=100)
    jproduk_cust: Optional[int] = None
    jproduk_stat_dok: Optional[Literal['Terbuka','Tertutup','Batal','Tunggu','Sementara','Semua']] = Query('Semua')
    timestamp_data: Optional[bool] = Field(default=False)

    @classmethod
    def as_form(
        cls,
        keywords: str = Query(None),
        page: int = Query(1, gt=0),
        results_per_page: int = Query(20, gt=0, le=100),
        jproduk_stat_dok: Literal['Terbuka','Tertutup','Batal','Tunggu','Sementara','Semua'] = Query('Semua', description="Status dokumen penjualan"),
        jproduk_cust: int = Query(None, description="`customer` dari API GET `/master/customer` (get_all_customer) -> key `cust_id`\n"),
        timestamp_data: bool = Query(False, description="Jika true, JSON akan disertakan detail timestamp."),
    ):
        return cls(
            keywords=keywords,
            page=page,
            results_per_page=results_per_page,
            jproduk_stat_dok=jproduk_stat_dok,
            jproduk_cust=jproduk_cust,
            timestamp_data=timestamp_data,
        )


class MasterJualProdukReqSchema(MasterJualProdukBaseDataSchema):
    jproduk_keterangan: Optional[str] = Field(default=None)
    jproduk_stat_dok: Optional[Literal['Terbuka','Tertutup','Batal','Tunggu','Sementara']] = Field(default='Terbuka')


class MasterJualProdukPutSchema(MasterJualProdukBaseDataSchema):
    jproduk_keterangan: Optional[str] = Field(default=None)
    jproduk_stat_dok: Optional[Literal['Terbuka','Tertutup','Batal','Tunggu','Sementara']] = Field(default='Terbuka')


class MasterJualProdukPatchSchema(MasterJualProdukBaseDataSchema):
    jproduk_tanggal: Optional[date] = None
    jproduk_cust: Optional[int] = None
    jproduk_diskon: Optional[float] = None
    jproduk_cara: Optional[Literal['tunai','card','transfer']] = 'tunai'
    jproduk_keterangan: Optional[str] = None
    jproduk_stat_dok: Optional[Literal['Terbuka','Tertutup','Batal','Tunggu','Sementara']] = 'Terbuka'
    jproduk_bayar: Optional[float] = None
    jproduk_totalbiaya: Optional[float] = None
