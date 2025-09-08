# ============================================= Start Noted Schema ===================================
# Author : PT. Dapur Perangkat Lunak Indonesia | KoffieSoft Group | https://www.koffiesoft.com/ | info@koffiesoft.com
# ============================================= END Noted Schema ===================================
from fastapi import Form, Query
from database import SessionLocal
from pydantic import BaseModel, Field, field_validator, model_validator
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
from enum import Enum
from datetime import date, datetime

class CustomerBaseDataSchema(BaseModel):
    cust_id: Optional[int] = None
    cust_no: str
    cust_nama_lengkap: str
    cust_nama_panggilan: Optional[str] = None
    cust_kelamin: Optional[Literal['L', 'P']] = None
    cust_alamat: Optional[str] = None
    cust_hp: Optional[str] = None
    cust_aktif: Literal['Aktif', 'Tidak Aktif'] = 'Aktif'
    cust_keterangan: Optional[str] = None


# =====================
# Response Schemas
# =====================
class CustomerListSchema(ResponseBaseSchema):
    data: List[CustomerBaseDataSchema]
    paging: List[PagingSchema]
    error: ErrorSchema
    request: RequestSchema


class CustomerSingleSchema(ResponseBaseSchema):
    data: CustomerBaseDataSchema
    error: ErrorSchema
    request: RequestSchema


# =====================
# Request List (Filter & Paging)
# =====================
class CustomerRequestListSchema(BaseModel):
    keywords: Optional[str] = Field(default=None)
    page: int = Field(default=1, gt=0)
    results_per_page: int = Field(default=20, gt=0, le=100)
    cust_aktif: Optional[Literal['Aktif', 'Tidak Aktif', 'Semua']] = Query('Semua')
    timestamp_data: Optional[bool] = Field(default=False)

    @classmethod
    def as_form(
        cls,
        keywords: str = Query(None),
        page: int = Query(1, gt=0),
        results_per_page: int = Query(20, gt=0, le=100),
        cust_aktif: Literal['Aktif', 'Tidak Aktif', 'Semua'] = Query('Semua', description="Status Customer"),
        timestamp_data: bool = Query(False, description="Jika true, JSON akan disertakan detail timestamp."),
    ):
        return cls(
            keywords=keywords,
            page=page,
            results_per_page=results_per_page,
            cust_aktif=cust_aktif,
            timestamp_data=timestamp_data,
        )


# =====================
# Create / Update Schemas
# =====================
class CustomerReqSchema(BaseModel):
    cust_no: str = Field(..., max_length=10, description="Kode pelanggan (maks 10 karakter)")
    cust_nama_lengkap: str = Field(..., min_length=1, max_length=100, description="Nama lengkap pelanggan")
    cust_nama_panggilan: Optional[str] = Field(None, max_length=50, description="Nama panggilan")
    cust_kelamin: Optional[Literal['L', 'P']] = Field(None, description="Jenis kelamin: L/P")
    cust_alamat: Optional[str] = Field(None, max_length=250, description="Alamat pelanggan")
    cust_hp: Optional[str] = Field(None, max_length=25, description="Nomor handphone")
    cust_aktif: Optional[Literal['Aktif', 'Tidak Aktif']] = Field(default='Aktif')
    cust_keterangan: Optional[str] = Field(None, max_length=1000, description="Keterangan tambahan")


class CustomerPutSchema(CustomerReqSchema):
    """Schema untuk update penuh (PUT)"""
    cust_no: str = Field(..., max_length=10)
    cust_nama_lengkap: str = Field(..., min_length=1)


class CustomerPatchSchema(BaseModel):
    """Schema untuk partial update (PATCH)"""
    cust_no: Optional[str] = Field(default=None, max_length=10)
    cust_nama_lengkap: Optional[str] = None
    cust_nama_panggilan: Optional[str] = None
    cust_kelamin: Optional[Literal['L', 'P']] = None
    cust_alamat: Optional[str] = None
    cust_hp: Optional[str] = None
    cust_aktif: Optional[Literal['Aktif', 'Tidak Aktif']] = None
    cust_keterangan: Optional[str] = None