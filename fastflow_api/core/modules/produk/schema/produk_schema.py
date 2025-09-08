# ============================================= Start Noted Schema ===================================
# Author : PT. Dapur Perangkat Lunak Indonesia | KoffieSoft Group | https://www.koffiesoft.com/ | info@koffiesoft.com
# ============================================= END Noted Schema ===================================
from fastapi import Form, Query
from database import SessionLocal
from pydantic import BaseModel, Field, field_validator, model_validator
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
from core.shared.base_validation_model_schema import validate_produk_group_by_id, validate_satuan_by_id

class ProdukBaseDataSchema(BaseModel):
    produk_sku: Optional[str] = None
    produk_group: Optional[int] = None
    produk_nama: str
    produk_satuan: int
    produk_harga: float = 0.0
    produk_diskon: float = 0.00
    produk_diskon_rp: float = 0.0
    produk_aktif: Literal['Aktif', 'Tidak Aktif'] = 'Aktif'
    produk_keterangan: Optional[str] = None

    # Field validator untuk memvalidasi produk_group
    @field_validator('produk_group')
    def validate_produk_group(cls, value):
        if value is not None:
            validate_produk_group_by_id(value)
        return value
    
    @field_validator('produk_satuan')
    def validate_produk_satuan(cls, value):
        if value is not None:
            validate_satuan_by_id(value)
        return value

    @model_validator(mode='after')
    def check_diskon_field_du(cls, values):
        produk_diskon = values.produk_diskon
        produk_diskon_rp = values.produk_diskon_rp

        if (produk_diskon not in [None, 0]) and (produk_diskon_rp not in [None, 0]):
            raise ValueError("Hanya boleh mengisi salah satu Diskon Umum: produk_diskon atau produk_diskon_rp.")

        return values

class ProdukListSchema(ResponseBaseSchema):
    data: List[ProdukBaseDataSchema]
    paging: List[PagingSchema]
    error: ErrorSchema
    request: RequestSchema

class ProdukSingleSchema(ResponseBaseSchema):
    data: ProdukBaseDataSchema
    error: ErrorSchema
    request: RequestSchema

class ProdukRequestListSchema(BaseModel):
    # Inisialisasi obj & set nilai default untuk validasi pydantic
    keywords: Optional[str] = Field(default=None)
    page: int = Field(default=1, gt=0)
    results_per_page: int = Field(default=20, gt=0, le=100)
    produk_sku: Optional[Union[int, str]] = None
    produk_group: Optional[int] = None
    produk_aktif: Optional[Literal['Aktif', 'Tidak Aktif', 'Semua']] = Query('Semua')
    produk_satuan_konversi_data: Optional[bool] = Field(default=False)
    produk_group_data: Optional[bool] = Field(default=False)
    timestamp_data: Optional[bool] = Field(default=False)

    # as form = membuat sebuah form untuk dokumentasi
    @classmethod
    def as_form(
        cls,
        keywords: str = Query(None),
        page: int = Query(1, gt=0),
        results_per_page: int = Query(20, gt=0, le=100),
        produk_sku: int = Query(None, description="`produk_sku` untuk pencarian produk by SKU \n"),
        produk_group: int = Query(None, description="`produk_group` dari API GET `/master/produk_group` (get_all_produk_group) -> key `group_id`\n"),
        produk_aktif: Literal['Aktif', 'Tidak Aktif', 'Semua'] = Query('Semua', description="Status Produk"),
        produk_satuan_konversi_data: bool = Query(False, description="Jika true, JSON akan disertakan detail satuan konversi."),
        produk_group_data: bool = Query(False, description="Jika true, JSON akan disertakan detail produk_group."),
        timestamp_data: bool = Query(False, description="Jika true, JSON akan disertakan detail timestamp."),
    ):
        return cls(
            keywords=keywords,
            page=page,
            results_per_page=results_per_page,
            produk_sku=produk_sku,
            produk_group=produk_group,
            produk_aktif=produk_aktif,
            produk_satuan_konversi_data=produk_satuan_konversi_data,
            produk_group_data=produk_group_data,
            timestamp_data=timestamp_data,
        )

class ProdukReqSchema(ProdukBaseDataSchema):
    pass

class ProdukPutSchema(ProdukBaseDataSchema):
    pass
    
class ProdukPatchSchema(BaseModel):
    produk_sku: Optional[str] = None
    produk_group: Optional[int] = None
    produk_nama: Optional[str] = None
    produk_satuan: Optional[int] = None
    produk_harga: Optional[float] = None
    produk_diskon: Optional[float] = None
    produk_diskon_rp: Optional[float] = None
    produk_aktif: Optional[Literal['Aktif', 'Tidak Aktif']] = None
    produk_keterangan: Optional[str] = None
