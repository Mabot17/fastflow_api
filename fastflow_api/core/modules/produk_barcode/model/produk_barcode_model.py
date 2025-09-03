# ============================================= Start Noted Model ===================================
# Author : Abdul Rohman Masrifan | masrifan26@gamil.com
# 1. Koneksi Table di database
# 2. Relasi Table di database bisa juga dilakukan disini
# ============================================= END Noted Model ===================================
from database import Base
from sqlalchemy import Column, String, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.sql.sqltypes import Integer, Float


class ProdukBarcodeModel(Base):
    __tablename__ = "products_header_alfa"

    productId = Column("productId", Integer, primary_key=True, index=True)
    productBarcode = Column("productBarcode", String(250))
    productName = Column("productName", String(25), unique=True)
    image = Column("image", String(250))
    sku = Column("sku", String(50))
    plu = Column("plu", String(250))
    categoryNameLvl0 = Column("categoryNameLvl0", String(50))
    categoryNameLvl1 = Column("categoryNameLvl1", String(50))
    categoryNameLvl2 = Column("categoryNameLvl2", String(50))
    categoryIdLvl0 = Column("categoryIdLvl0", String(250))
    categoryIdLvl1 = Column("categoryIdLvl1", String(250))
    categoryIdLvl2 = Column("categoryIdLvl2", String(250))
    stock = Column("stock", Integer)
    basePrice = Column("basePrice", Float)
    finalPrice = Column("finalPrice", Float)
    discountPercent = Column("discountPercent", Float)
    discountQty = Column("discountQty", Float)
    discountPrice = Column("discountPrice", Float)
    discountValue = Column("discountValue", Float)
    aktif = Column("aktif", String(250))
    keterangan = Column("keterangan", String(250))

    revised = Column("revised", Integer)
    created_by = Column("created_by", String(100))
    created_at = Column("created_at", DateTime)
    updated_by = Column("updated_by", String(100))
    updated_at = Column("updated_at", DateTime)
    deleted_by = Column("deleted_by", String(100))
    deleted_at = Column("deleted_at", DateTime)
