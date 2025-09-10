# ============================================= Start Noted Model ===================================
# Author : PT. Dapur Perangkat Lunak Indonesia | KoffieSoft Group | https://www.koffiesoft.com/ | info@koffiesoft.com
# 1. Koneksi Table di database
# 2. Relasi Table di database bisa juga dilakukan disini
# ============================================= END Noted Model ===================================
from database import Base
from sqlalchemy import Column, String, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.sql.schema import ForeignKey
from sqlalchemy.sql.sqltypes import Integer, Float, SmallInteger, Enum, DECIMAL


class ProdukModel(Base):
    __tablename__ = "produk"

    produk_id = Column(Integer, primary_key=True, autoincrement=True, index=True)
    produk_kode = Column(String(20), unique=True, nullable=False)
    produk_sku = Column(String(100), nullable=True)  # sku satuan terkecil
    produk_group = Column(Integer, ForeignKey("produk_group.group_id"), nullable=True)
    produk_nama = Column(String(250), nullable=False)
    produk_satuan = Column(Integer, ForeignKey("satuan.satuan_id"), nullable=True)
    produk_harga = Column(Float, nullable=False, default=0.0)  # harga satuan default
    produk_diskon = Column(DECIMAL(10, 2), nullable=False, default=0.00)
    produk_diskon_rp = Column(Float, nullable=False, default=0.0)
    produk_foto_path = Column(String(1000), nullable=True)
    produk_aktif = Column(Enum("Aktif", "Tidak Aktif"), default="Aktif")
    produk_keterangan = Column(String(500), nullable=True)

    revised = Column("revised", Integer)
    created_by = Column("created_by", String(100))
    created_at = Column("created_at", DateTime)
    updated_by = Column("updated_by", String(100))
    updated_at = Column("updated_at", DateTime)
    deleted_by = Column("deleted_by", String(100))
    deleted_at = Column("deleted_at", DateTime)

    # Relasi Satuan
    produk_satuan_data = relationship("SatuanModel", foreign_keys=[produk_satuan], back_populates="produk_satuan_model_data")

    # Relasi Detail Dari Produk
    produk_satuan_konversi_data = relationship("SatuanKonversiModel", back_populates="produk_satuan_konversi_model_data")
    produk_group_data = relationship("ProdukGroupModel", back_populates="produk_group_model_data")

    dproduk_produk_model_data = relationship("DetailJualProdukModel", back_populates="dproduk_produk_data")