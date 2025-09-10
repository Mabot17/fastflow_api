# ============================================= Start Noted Model ===================================
# Author : PT. Dapur Perangkat Lunak Indonesia | KoffieSoft Group | https://www.koffiesoft.com/ | info@koffiesoft.com
# 1. Koneksi Table di database
# 2. Relasi Table di database bisa juga dilakukan disini
# ============================================= END Noted Model ===================================
from database import Base
from sqlalchemy import Column, String, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.sql.schema import ForeignKey
from sqlalchemy.sql.sqltypes import Integer, Float


class DetailJualProdukModel(Base):
    __tablename__ = "detail_jual_produk"

    dproduk_id = Column("dproduk_id", Integer, primary_key=True, index=True)
    dproduk_master = Column("dproduk_master", Integer)
    dproduk_produk = Column("dproduk_produk", Integer, ForeignKey("produk.produk_id"))
    dproduk_satuan = Column("dproduk_satuan", Integer, ForeignKey("satuan.satuan_id"))
    dproduk_jumlah = Column("dproduk_jumlah", Integer)
    dproduk_harga = Column("dproduk_harga", String(20))
    dproduk_diskon = Column("dproduk_diskon", String(250))
    dproduk_diskon_rp = Column("dproduk_diskon_rp", String(250))

    revised = Column("revised", Integer)
    created_by = Column("created_by", String(100))
    created_at = Column("created_at", DateTime)
    updated_by = Column("updated_by", String(100))
    updated_at = Column("updated_at", DateTime)
    deleted_by = Column("deleted_by", String(100))
    deleted_at = Column("deleted_at", DateTime)

    dproduk_satuan_data = relationship("SatuanModel", back_populates="dproduk_satuan_model_data")
    dproduk_produk_data = relationship("ProdukModel", back_populates="dproduk_produk_model_data")