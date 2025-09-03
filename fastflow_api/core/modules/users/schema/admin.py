from core.config import ZONA_WAKTU_SERVER
from datetime import datetime, date
from pydantic import BaseModel, EmailStr
from typing import Optional, List
from enum import Enum
from core.shared.base import (
    DaftarBaseSchema,
    PagingSchema,
    StatusSchema,
    StatusResponseSchema,
    ResponseBaseSchema,
    JenisKelamin,
    StatusRecord,
)


class UserAdminRole(str, Enum):
    superadmin = "superadmin"
    admin = "admin"


class UserAdminBaseSchema(BaseModel):
    email: EmailStr
    hp: str
    firstname: str
    lastname: str
    role: Optional[UserAdminRole] = None
    tgl_lahir: Optional[date] = None
    jenis_kelamin: Optional[JenisKelamin] = None
    status: Optional[StatusRecord] = None

    class Config:
        # orm_mode = True
        from_attributes = True


class UserAdminReqSchema(UserAdminBaseSchema):
    password: str


class UserAdminChangePasswordSchema(BaseModel):
    password: str


class UserAdminRespBaseSchema(UserAdminBaseSchema):
    id: int
    status: Optional[StatusSchema]


class UserAdminRespSchema(ResponseBaseSchema):
    status: StatusResponseSchema
    data: UserAdminRespBaseSchema


class DaftarUserAdminSchema(DaftarBaseSchema):
    status: StatusResponseSchema
    paging: PagingSchema
    data: List[UserAdminRespBaseSchema]


class UserAdminGantiRoleSchema(BaseModel):
    role: UserAdminRole
