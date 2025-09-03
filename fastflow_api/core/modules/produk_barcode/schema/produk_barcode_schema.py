# ============================================= Start Noted Schema ===================================
# Author : Abdul Rohman Masrifan | masrifan26@gamil.com
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

class ProdukBarcodeBaseDataSchema(BaseModel):
    # id: int
    productBarcode: str

class ProdukBarcodeListSchema(ResponseBaseSchema):
    data: List[ProdukBarcodeBaseDataSchema]
    paging: List[PagingSchema]
    error: ErrorSchema
    request: RequestSchema

class ProdukBarcodeSingleSchema(ResponseBaseSchema):
    data: ProdukBarcodeBaseDataSchema
    error: ErrorSchema
    request: RequestSchema

class ProdukBarcodeRequestListSchema(BaseModel):
    # Inisialisasi obj & set nilai default untuk validasi pydantic
    keywords: Optional[str] = Field(default=None)
    page: int = Field(default=1, gt=0)
    results_per_page: int = Field(default=20, gt=0, le=100)
    aktif: Optional[Literal['Aktif', 'Tidak Aktif', 'Semua']] = Field('Semua')
    categoryId: Optional[str] = None
    timestamp_data: Optional[bool] = Field(default=False)

    # as form = membuat sebuah form untuk dokumentasi
    @classmethod
    def as_form(
        cls,
        keywords: str = Query(None),
        page: int = Query(1, gt=0),
        results_per_page: int = Query(20, gt=0, le=100),
        aktif: Literal['Aktif', 'Tidak Aktif', 'Semua'] = Query('Semua', description="Status ProdukBarcode"),
        categoryId: str = Query(None, description="Kategori"),
        timestamp_data: bool = Query(False, description="Jika true, JSON akan disertakan detail timestamp."),
    ):
        return cls(
            keywords=keywords,
            page=page,
            results_per_page=results_per_page,
            aktif=aktif,
            categoryId=categoryId,
            timestamp_data=timestamp_data,
        )

class ProdukBarcodeReqSchema(ProdukBarcodeBaseDataSchema):
    # Inisialisasi obj & set nilai default untuk validasi pydantic
    # Disini akan memodifikasi nilai dari induknya ProdukBarcodeBaseDataSchema, jika didefinisikan ulang dibawah seperti berikut
    keterangan: Optional[str] = Field(default=None)
    aktif: Optional[Literal['Aktif', 'Tidak Aktif']] = Field(default='Aktif')

class ProdukBarcodePutSchema(ProdukBarcodeBaseDataSchema):
    # Inisialisasi obj & set nilai default untuk validasi pydantic
    # Disini akan memodifikasi nilai dari induknya ProdukBarcodeBaseDataSchema, jika didefinisikan ulang dibawah seperti berikut
    keterangan: Optional[str] = Field(default=None)
    aktif: Optional[Literal['Aktif', 'Tidak Aktif']] = Field(default='Aktif')

    
class ProdukBarcodePatchSchema(ProdukBarcodeBaseDataSchema):
    # Inisialisasi obj & set nilai default untuk validasi pydantic menjadi None semua, karena method patch
    productBarcode: Optional[str] = Field(default=None)
    productName: Optional[str] = Field(default=None)
    keterangan: Optional[str] = Field(default=None)
    aktif: Optional[Literal['Aktif', 'Tidak Aktif']] = Field(default='Aktif')