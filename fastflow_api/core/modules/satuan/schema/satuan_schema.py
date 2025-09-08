# ============================================= Start Noted Schema ===================================
# Author : PT. Dapur Perangkat Lunak Indonesia | KoffieSoft Group | https://www.koffiesoft.com/ | info@koffiesoft.com
# ============================================= END Noted Schema ===================================
from fastapi import Form, Query
from database import SessionLocal
from pydantic import BaseModel, Field, validator
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

class SatuanBaseDataSchema(BaseModel):
    # satuan_id: int
    satuan_kode: str
    satuan_nama: str
    satuan_keterangan: str = None
    satuan_aktif: Literal['Aktif', 'Tidak Aktif'] = 'Aktif'

class SatuanListSchema(ResponseBaseSchema):
    data: List[SatuanBaseDataSchema]
    paging: List[PagingSchema]
    error: ErrorSchema
    request: RequestSchema

class SatuanSingleSchema(ResponseBaseSchema):
    data: SatuanBaseDataSchema
    error: ErrorSchema
    request: RequestSchema

class SatuanRequestListSchema(BaseModel):
    # Inisialisasi obj & set nilai default untuk validasi pydantic
    keywords: Optional[str] = Field(default=None)
    page: int = Field(default=1, gt=0)
    results_per_page: int = Field(default=20, gt=0, le=100)
    satuan_aktif: Optional[Literal['Aktif', 'Tidak Aktif', 'Semua']] = Query('Semua')
    timestamp_data: Optional[bool] = Field(default=False)

    # as form = membuat sebuah form untuk dokumentasi
    @classmethod
    def as_form(
        cls,
        keywords: str = Query(None),
        page: int = Query(1, gt=0),
        results_per_page: int = Query(20, gt=0, le=100),
        satuan_aktif: Literal['Aktif', 'Tidak Aktif', 'Semua'] = Query('Semua', description="Status Satuan"),
        timestamp_data: bool = Query(False, description="Jika true, JSON akan disertakan detail timestamp."),
    ):
        return cls(
            keywords=keywords,
            page=page,
            results_per_page=results_per_page,
            satuan_aktif=satuan_aktif,
            timestamp_data=timestamp_data,
        )

class SatuanReqSchema(SatuanBaseDataSchema):
    # Inisialisasi obj & set nilai default untuk validasi pydantic
    # Disini akan memodifikasi nilai dari induknya SatuanBaseDataSchema, jika didefinisikan ulang dibawah seperti berikut
    satuan_keterangan: Optional[str] = Field(default=None)
    satuan_aktif: Optional[Literal['Aktif', 'Tidak Aktif']] = Field(default='Aktif')

class SatuanPutSchema(SatuanBaseDataSchema):
    # Inisialisasi obj & set nilai default untuk validasi pydantic
    # Disini akan memodifikasi nilai dari induknya SatuanBaseDataSchema, jika didefinisikan ulang dibawah seperti berikut
    satuan_keterangan: Optional[str] = Field(default=None)
    satuan_aktif: Optional[Literal['Aktif', 'Tidak Aktif']] = Field(default='Aktif')

    
class SatuanPatchSchema(SatuanBaseDataSchema):
    # Inisialisasi obj & set nilai default untuk validasi pydantic menjadi None semua, karena method patch
    satuan_kode: Optional[str] = Field(default=None)
    satuan_nama: Optional[str] = Field(default=None)
    satuan_keterangan: Optional[str] = Field(default=None)
    satuan_aktif: Optional[Literal['Aktif', 'Tidak Aktif']] = Field(default='Aktif')