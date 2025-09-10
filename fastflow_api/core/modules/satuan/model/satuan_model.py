# ============================================= Start Noted Model ===================================
# Author : PT. Dapur Perangkat Lunak Indonesia | KoffieSoft Group | https://www.koffiesoft.com/ | info@koffiesoft.com
# 1. Koneksi Table di database
# 2. Relasi Table di database bisa juga dilakukan disini
# ============================================= END Noted Model ===================================
from database import Base
from sqlalchemy import Column, String, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.sql.sqltypes import Integer


class SatuanModel(Base):
    __tablename__ = "satuan"

    satuan_id = Column("satuan_id", Integer, primary_key=True, index=True)
    satuan_kode = Column("satuan_kode", String(25), unique=True)
    satuan_nama = Column("satuan_nama", String(250))
    satuan_aktif = Column("satuan_aktif", String(20))
    satuan_keterangan = Column("satuan_keterangan", String(250))

    revised = Column("revised", Integer)
    created_by = Column("created_by", String(100))
    created_at = Column("created_at", DateTime)
    updated_by = Column("updated_by", String(100))
    updated_at = Column("updated_at", DateTime)
    deleted_by = Column("deleted_by", String(100))
    deleted_at = Column("deleted_at", DateTime)

    # Relasi Master Produk
    produk_satuan_model_data = relationship(
        "ProdukModel",
        back_populates="produk_satuan_data",
        foreign_keys="[ProdukModel.produk_satuan]"
    )

    # Relasi Satuan Konversi
    konversi_satuan_model_data = relationship("SatuanKonversiModel", back_populates="konversi_satuan_data")

    dproduk_satuan_model_data = relationship("DetailJualProdukModel", back_populates="dproduk_satuan_data")