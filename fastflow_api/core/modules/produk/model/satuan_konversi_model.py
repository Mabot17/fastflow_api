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


class SatuanKonversiModel(Base):
    __tablename__ = "satuan_konversi"

    konversi_id = Column("konversi_id", Integer, primary_key=True, index=True)
    konversi_sku = Column("konversi_sku", String(250))
    konversi_produk = Column("konversi_produk", Integer, ForeignKey("produk.produk_id"))
    konversi_satuan = Column("konversi_satuan", Integer, ForeignKey("satuan.satuan_id"))
    konversi_nilai = Column("konversi_nilai", Float)
    konversi_harga = Column("konversi_harga", Float)
    konversi_keterangan = Column("konversi_keterangan", String(250))
    konversi_aktif = Column("konversi_aktif", String(20))
    konversi_default = Column("konversi_default", String(20))

    revised = Column("revised", Integer)
    created_by = Column("created_by", String(100))
    created_at = Column("created_at", DateTime)
    updated_by = Column("updated_by", String(100))
    updated_at = Column("updated_at", DateTime)
    deleted_by = Column("deleted_by", String(100))
    deleted_at = Column("deleted_at", DateTime)

    # Relasi Master Produk
    produk_satuan_konversi_model_data = relationship("ProdukModel", back_populates="produk_satuan_konversi_data")

    konversi_satuan_data = relationship("SatuanModel", back_populates="konversi_satuan_model_data")