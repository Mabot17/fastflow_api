from pydantic import BaseModel
from typing import Optional, List
from enum import Enum


class PagingSchema(BaseModel):
    page: int
    total_pages: int
    records_per_page: int
    total_records: int

class ErrorSchema(BaseModel):
    List

class RequestSchema(BaseModel):
    List

class StatusSchema(BaseModel):
    code: str
    message: str


class StatusResponseSchema(BaseModel):
    code: str
    message: str


class PrimaryRecordSchema(BaseModel):
    code: str
    message: str


class DaftarBaseSchema(BaseModel):
    paging: Optional[PagingSchema]


class ResponseBaseSchema(BaseModel):
    status: StatusResponseSchema


class StatusRecord(int, Enum):
    deleted = -1
    nonaktif = 0
    aktif = 1

class StatusStringRecord(Enum):
    aktif = 'Aktif'
    nonaktif = 'Tidak Aktif'

class StatusArtikel(int, Enum):
    draft = 0
    published = 1
    unpublished = 2


class ImageQuality(Enum):
    THUMBNAIL = "thumbnail"
    MEDIUM = "medium"
    HIGH = "high"


class VideoStorage(str, Enum):
    INTERNAL = "internal"
    AWS_S3 = "aws_s3"


class PhotoStorage(str, Enum):
    INTERNAL = "internal"
    AWS_S3 = "aws_s3"


class SearchEngine(str, Enum):
    SIMPLE_QUERY = "simple_query"
    FULL_TEXT = "full_text"
    ALGOLIA = "algolia"


class JenisKelamin(int, Enum):
    LAKI_LAKI = 1
    PEREMPUAN = 2


class ZonaWaktuIndonesia(Enum):
    WIB = "wib"
    WITA = "wita"
    WIT = "wit"
