# ============================================= Start Noted Model ===================================
# Author : PT. Dapur Perangkat Lunak Indonesia | KoffieSoft Group | https://www.koffiesoft.com/ | info@koffiesoft.com
# 1. Koneksi Table di database
# 2. Relasi Table di database bisa juga dilakukan disini
# ============================================= END Noted Model ===================================
from database import Base
from sqlalchemy import Column, String, DateTime, Enum
from sqlalchemy.orm import relationship
from sqlalchemy.sql.schema import ForeignKey
from sqlalchemy.sql.sqltypes import Integer, Float, Double


class MasterJualProdukModel(Base):
    __tablename__ = "master_jual_produk"

    jproduk_id = Column("jproduk_id", Integer, primary_key=True, index=True)
    jproduk_nobukti = Column("jproduk_nobukti", String(250))
    jproduk_cust = Column("jproduk_cust", Integer, ForeignKey("customer.cust_id"))
    jproduk_tanggal = Column("jproduk_tanggal", DateTime)
    jproduk_diskon = Column("jproduk_diskon", Float)
    jproduk_cara = Column("jproduk_cara", String(50))
    jproduk_stat_dok = Column("jproduk_stat_dok", String(50))
    jproduk_bayar = Column("jproduk_bayar", Integer)
    jproduk_totalbiaya = Column("jproduk_totalbiaya", Float)
    jproduk_keterangan = Column("jproduk_keterangan", String(250))

    revised = Column("revised", Integer)
    created_by = Column("created_by", String(100))
    created_at = Column("created_at", DateTime)
    updated_by = Column("updated_by", String(100))
    updated_at = Column("updated_at", DateTime)
    deleted_by = Column("deleted_by", String(100))
    deleted_at = Column("deleted_at", DateTime)

    jproduk_cust_data = relationship("CustomerModel", foreign_keys=[jproduk_cust], back_populates="jproduk_cust_model_data")
