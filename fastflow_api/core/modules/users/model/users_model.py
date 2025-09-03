from sqlalchemy.orm import relationship
from sqlalchemy.sql.schema import ForeignKey
from sqlalchemy.sql.sqltypes import Date, Integer
from database import Base
from sqlalchemy import Column, BigInteger, String, DateTime, SmallInteger
from sqlalchemy.orm import Session


class UsersModel(Base):
    __tablename__ = "users"

    user_id = Column("user_id", BigInteger, primary_key=True, index=True)
    user_name = Column("user_name", String(255))
    user_password = Column("user_password", String(255))
    user_kode = Column("user_kode", String(255))
    user_keterangan = Column("user_keterangan", String(255))
    user_aktif = Column("user_aktif", String(25))
    user_otp_code = Column("user_otp_code", String(255))

    revised = Column("revised", Integer)
    created_by = Column("created_by", String(100))
    created_at = Column("created_at", DateTime)
    updated_by = Column("updated_by", String(100))
    updated_at = Column("updated_at", DateTime)
    deleted_by = Column("deleted_by", String(100))
    deleted_at = Column("deleted_at", DateTime)
