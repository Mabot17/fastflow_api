# ============================================= Start Noted Schema ===================================
# Author : PT. Dapur Perangkat Lunak Indonesia | KoffieSoft Group | https://www.koffiesoft.com/ | info@koffiesoft.com
# ============================================= END Noted Schema ===================================
from fastapi import Form, Query
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
from core.shared.base_validation_model_schema import validate_produk_by_id, validate_satuan_by_id
from enum import Enum

class SatuanKonversiBaseDataSchema(BaseModel):
    # konversi_id: int
    konversi_satuan: int
    konversi_sku: str = None
    konversi_nilai: float = 0.0
    konversi_harga: float = 0.0
    konversi_keterangan: str = None
    konversi_aktif: Literal['Aktif', 'Tidak Aktif'] = 'Aktif'
    konversi_default: Literal["true", "false"] = "false"

    # Field validator untuk memvalidasi konversi_satuan
    @field_validator('konversi_satuan')
    def validate_satuan(cls, value):
        if value is not None:
            validate_satuan_by_id(value)
        return value


class SatuanKonversiListSchema(ResponseBaseSchema):
    data: List[SatuanKonversiBaseDataSchema]
    paging: List[PagingSchema]
    error: ErrorSchema
    request: RequestSchema

class SatuanKonversiSingleSchema(ResponseBaseSchema):
    data: SatuanKonversiBaseDataSchema
    error: ErrorSchema
    request: RequestSchema

class SatuanKonversiRequestListSchema(BaseModel):
    # Inisialisasi obj & set nilai default untuk validasi pydantic
    keywords: Optional[str] = Field(default=None)
    page: int = Field(default=1, gt=0)
    results_per_page: int = Field(default=20, gt=0, le=100)
    konversi_aktif: Optional[Literal['Aktif', 'Tidak Aktif', 'Semua']] = Query('Semua')
    konversi_satuan_data: Optional[bool] = Field(default=False)
    timestamp_data: Optional[bool] = Field(default=False)

    # as form = membuat sebuah form untuk dokumentasi
    @classmethod
    def as_form(
        cls,
        keywords: str = Query(None),
        page: int = Query(1, gt=0),
        results_per_page: int = Query(20, gt=0, le=100),
        konversi_aktif: Literal['Aktif', 'Tidak Aktif', 'Semua'] = Query('Semua', description="Status Satuan Konversi"),
        konversi_satuan_data: bool = Query(False, description="Jika true, JSON akan disertakan detail satuan."),
        timestamp_data: bool = Query(False, description="Jika true, JSON akan disertakan detail timestamp."),
    ):
        return cls(
            keywords=keywords,
            page=page,
            results_per_page=results_per_page,
            konversi_aktif=konversi_aktif,
            konversi_satuan_data=konversi_satuan_data,
            timestamp_data=timestamp_data,
        )

class SatuanKonversiReqSchema(SatuanKonversiBaseDataSchema):
    # Inisialisasi obj & set nilai default untuk validasi pydantic
    # Disini akan memodifikasi nilai dari induknya SatuanKonversiBaseDataSchema, jika didefinisikan ulang dibawah seperti berikut
    konversi_keterangan: Optional[str] = Field(default=None)
    konversi_aktif: Optional[Literal['Aktif', 'Tidak Aktif']] = Field(default='Aktif')
    konversi_default: Optional[Literal["true", "false"]] = "false"

    
class SatuanKonversiPatchSchema(SatuanKonversiBaseDataSchema):
    # Inisialisasi obj & set nilai default untuk validasi pydantic menjadi None semua, karena method patch
    konversi_sku: Optional[str] = Field(default=None)
    konversi_satuan: Optional[int] = Field(default=None)
    konversi_keterangan: Optional[str] = Field(default=None)
    konversi_harga: Optional[float] = Field(default=0)
    konversi_aktif: Optional[Literal['Aktif', 'Tidak Aktif']] = Field(default='Aktif')
    konversi_default: Optional[Literal["true", "false"]] = "false"