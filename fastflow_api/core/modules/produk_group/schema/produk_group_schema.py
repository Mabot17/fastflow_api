# ============================================= Start Noted Schema ===================================
# Author : PT. Dapur Perangkat Lunak Indonesia | KoffieSoft Group | https://www.koffiesoft.com/ | info@koffiesoft.com
# ============================================= END Noted Schema ===================================
from fastapi import Form, Query
from database import SessionLocal
from pydantic import BaseModel, Field, field_validator, constr
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

class ProdukGroupBaseDataSchema(BaseModel):
    # group_id: int
    group_kode: str
    group_nama: str
    group_keterangan: str = None
    group_aktif: Literal['Aktif', 'Tidak Aktif'] = 'Aktif'

    @field_validator('group_kode', 'group_nama')
    def tidak_boleh_kosong(cls, v, field):
        if not v or not v.strip():
            raise ValueError(f"{field.field_name} tidak boleh kosong atau hanya spasi")
        return v

class ProdukGroupListSchema(ResponseBaseSchema):
    data: List[ProdukGroupBaseDataSchema]
    paging: List[PagingSchema]
    error: ErrorSchema
    request: RequestSchema

class ProdukGroupSingleSchema(ResponseBaseSchema):
    data: ProdukGroupBaseDataSchema
    error: ErrorSchema
    request: RequestSchema

class ProdukGroupRequestListSchema(BaseModel):
    # Inisialisasi obj & set nilai default untuk validasi pydantic
    keywords: Optional[str] = Field(default=None)
    page: int = Field(default=1, gt=0)
    results_per_page: int = Field(default=20, gt=0, le=100)
    group_aktif: Optional[Literal['Aktif', 'Tidak Aktif', 'Semua']] = Query('Semua')
    timestamp_data: Optional[bool] = Field(default=False)

    # as form = membuat sebuah form untuk dokumentasi
    @classmethod
    def as_form(
        cls,
        keywords: str = Query(None),
        page: int = Query(1, gt=0),
        results_per_page: int = Query(20, gt=0, le=100),
        group_aktif: Literal['Aktif', 'Tidak Aktif', 'Semua'] = Query('Semua', description="Status ProdukGroup"),
        timestamp_data: bool = Query(False, description="Jika true, JSON akan disertakan detail timestamp."),
    ):
        return cls(
            keywords=keywords,
            page=page,
            results_per_page=results_per_page,
            group_aktif=group_aktif,
            timestamp_data=timestamp_data,
        )

class ProdukGroupReqSchema(ProdukGroupBaseDataSchema):
    # Inisialisasi obj & set nilai default untuk validasi pydantic
    # Disini akan memodifikasi nilai dari induknya ProdukGroupBaseDataSchema, jika didefinisikan ulang dibawah seperti berikut
    group_keterangan: Optional[str] = Field(default=None)
    group_aktif: Optional[Literal['Aktif', 'Tidak Aktif']] = Field(default='Aktif')

class ProdukGroupPutSchema(ProdukGroupBaseDataSchema):
    # Inisialisasi obj & set nilai default untuk validasi pydantic menjadi None semua, karena method patch
    group_kode: str = Field(default=None, max_length=5)
    group_nama: str = Field(default=None)
    group_keterangan: str = Field(default=None)
    group_aktif: Literal['Aktif', 'Tidak Aktif'] = Field(default='Aktif')

class ProdukGroupPatchSchema(ProdukGroupBaseDataSchema):
    # Inisialisasi obj & set nilai default untuk validasi pydantic menjadi None semua, karena method patch
    group_kode: Optional[str] = Field(default=None, max_length=5)
    group_nama: Optional[str] = Field(default=None)
    group_keterangan: Optional[str] = Field(default=None)
    group_aktif: Optional[Literal['Aktif', 'Tidak Aktif']] = Field(default='Aktif')