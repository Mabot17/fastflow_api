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
from core.shared.base_validation_model_schema import validate_produk_by_id, validate_satuan_konversi_produk_by_id, validate_satuan_by_id
from enum import Enum

class DetailMasterJualProdukBaseDataSchema(BaseModel):
    # dproduk_id: intpenerimaan_barang
    dproduk_produk: int
    dproduk_satuan: int
    dproduk_jumlah: float = 0.0
    dproduk_harga: float = 0.0
    dproduk_diskon: float = 0.0
    dproduk_diskon_rp: float = 0.0

    # Field validator untuk memvalidasi dproduk_produk
    @field_validator('dproduk_produk')
    def validate_produk(cls, value):
        if value is not None:
            validate_produk_by_id(value)
        return value
    
    @field_validator('dproduk_satuan')
    def validate_satuan(cls, value):
        if value is not None:
            # Hanya validasi dasar di sini.
            validate_satuan_by_id(value)
        return value

    @model_validator(mode='after')
    def validate_satuan_konversi(cls, values):
        produk_id = values.dproduk_produk  # Gunakan atribut langsung
        satuan_id = values.dproduk_satuan

        if produk_id and satuan_id:
            validate_satuan_konversi_produk_by_id(produk_id, satuan_id)

        return values

class DetailMasterJualProdukListSchema(ResponseBaseSchema):
    data: List[DetailMasterJualProdukBaseDataSchema]
    paging: List[PagingSchema]
    error: ErrorSchema
    request: RequestSchema

class DetailMasterJualProdukSingleSchema(ResponseBaseSchema):
    data: DetailMasterJualProdukBaseDataSchema
    error: ErrorSchema
    request: RequestSchema

class DetailMasterJualProdukRequestListSchema(BaseModel):
    # Inisialisasi obj & set nilai default untuk validasi pydantic
    keywords: Optional[str] = Field(default=None)
    page: int = Field(default=1, gt=0)
    results_per_page: int = Field(default=20, gt=0, le=100)
    dproduk_produk_data: Optional[bool] = Field(default=False)
    dproduk_satuan_data: Optional[bool] = Field(default=False)
    timestamp_data: Optional[bool] = Field(default=False)

    # as form = membuat sebuah form untuk dokumentasi
    @classmethod
    def as_form(
        cls,
        page: int = Query(1, gt=0),
        results_per_page: int = Query(20, gt=0, le=100),
        dproduk_produk_data: bool = Query(False, description="Jika true, JSON akan disertakan detail gudang."),
        dproduk_satuan_data: bool = Query(False, description="Jika true, JSON akan disertakan detail gudang."),
        timestamp_data: bool = Query(False, description="Jika true, JSON akan disertakan detail timestamp."),
    ):
        return cls(
            page=page,
            results_per_page=results_per_page,
            dproduk_produk_data=dproduk_produk_data,
            dproduk_satuan_data=dproduk_satuan_data,
            timestamp_data=timestamp_data,
        )

class DetailMasterJualProdukReqSchema(DetailMasterJualProdukBaseDataSchema):
    # Inisialisasi obj & set nilai default untuk validasi pydantic
    # Disini akan memodifikasi nilai dari induknya DetailMasterJualProdukBaseDataSchema, jika didefinisikan ulang dibawah seperti berikut
    dproduk_harga: Optional[float] = Field(default=None)
    dproduk_jumlah: Optional[float] = Field(default=None)
    dproduk_diskon: Optional[float] = Field(default=None)
    dproduk_diskon_rp: Optional[float] = Field(default=None)

    
class DetailMasterJualProdukPatchSchema(DetailMasterJualProdukBaseDataSchema):
    # Inisialisasi obj & set nilai default untuk validasi pydantic menjadi None semua, karena method patch
    dproduk_produk: Optional[int] = Field(default=None)
    dproduk_satuan: Optional[int] = Field(default=None)
    dproduk_harga: Optional[float] = Field(default=None)
    dproduk_jumlah: Optional[float] = Field(default=None)
    dproduk_diskon: Optional[float] = Field(default=None)
    dproduk_diskon_rp: Optional[float] = Field(default=None)