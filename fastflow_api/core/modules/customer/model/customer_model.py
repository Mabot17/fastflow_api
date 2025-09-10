# ============================================= Start Noted Model ===================================
# Author : PT. Dapur Perangkat Lunak Indonesia | KoffieSoft Group | https://www.koffiesoft.com/ | info@koffiesoft.com
# 1. Koneksi Table di database
# 2. Relasi Table di database bisa juga dilakukan disini
# ============================================= END Noted Model ===================================
from database import Base
from sqlalchemy import Column, String, DateTime, Enum, Date, Float, SmallInteger
from sqlalchemy.orm import relationship
from sqlalchemy.sql.sqltypes import Integer
from sqlalchemy.sql.schema import ForeignKey


class CustomerModel(Base):
    __tablename__ = "customer"

    cust_id             = Column(Integer, primary_key=True, index=True, autoincrement=True)
    cust_no             = Column(String(50), index=True)
    cust_nama_lengkap   = Column(String(100, collation="utf8_general_ci"))
    cust_nama_panggilan = Column(String(50))
    cust_kelamin        = Column(Enum('L', 'P'))
    cust_alamat         = Column(String(250))
    cust_hp             = Column(String(25))
    cust_aktif          = Column(Enum('Aktif', 'Tidak Aktif'), default="Aktif", nullable=False)
    cust_keterangan     = Column(String(1000))

    revised = Column("revised", Integer)
    created_by = Column("created_by", String(100))
    created_at = Column("created_at", DateTime)
    updated_by = Column("updated_by", String(100))
    updated_at = Column("updated_at", DateTime)
    deleted_by = Column("deleted_by", String(100))
    deleted_at = Column("deleted_at", DateTime)

    # Relasi Master Jual Produk
    jproduk_cust_model_data = relationship("MasterJualProdukModel", back_populates="jproduk_cust_data")