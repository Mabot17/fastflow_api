# ============================================= Start Noted Model ===================================
# Author : PT. Dapur Perangkat Lunak Indonesia | KoffieSoft Group | https://www.koffiesoft.com/ | info@koffiesoft.com
# 1. Koneksi Table di database
# 2. Relasi Table di database bisa juga dilakukan disini
# ============================================= END Noted Model ===================================
from database import Base
from sqlalchemy import Column, String, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.sql.sqltypes import Integer


class ProdukGroupModel(Base):
    __tablename__ = "produk_group"

    group_id = Column("group_id", Integer, primary_key=True, index=True)
    group_kode = Column("group_kode", String(25), unique=True)
    group_nama = Column("group_nama", String(250))
    group_aktif = Column("group_aktif", String(20))
    group_keterangan = Column("group_keterangan", String(250))

    revised = Column("revised", Integer)
    created_by = Column("created_by", String(100))
    created_at = Column("created_at", DateTime)
    updated_by = Column("updated_by", String(100))
    updated_at = Column("updated_at", DateTime)
    deleted_by = Column("deleted_by", String(100))
    deleted_at = Column("deleted_at", DateTime)

    # Relasi Master Produk
    produk_group_model_data = relationship("ProdukModel", back_populates="produk_group_data")