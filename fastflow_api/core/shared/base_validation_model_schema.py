"""
============================================= Start Noted Validasi ===================================
Author : Abdul Rohman Masrifan | https://fastflow.pybot.cloud/ | masrifan26@gmail.com
1. Menggunakan SQLAlchemy ORM Session untuk validasi global
============================================= END Noted Validasi ===================================
"""

from sqlalchemy.orm import Session
from core.modules.master.produk_group.model.produk_group_model import ProdukGroupModel
from core.modules.master.produk_group.model.produk_group_sub_model import ProdukGroupSubModel
from core.modules.master.produk.model.produk_model import ProdukModel
from core.modules.master.produk.model.satuan_konversi_model import SatuanKonversiModel
from core.modules.master.satuan.model.satuan_model import SatuanModel
from core.modules.master.gudang.model.gudang_model import GudangModel
from core.modules.master.supplier.model.supplier_model import SupplierModel
from core.modules.master.customer.model.customer_model import CustomerModel
from database import SessionLocal

def validate_gudang_by_id(gudang_id: int) -> bool:
    """
    Untuk memvalidasi keberadaan gudang berdasarkan ID
    """
    db: Session = SessionLocal()
    try:
        # Query untuk memeriksa keberadaan gudang yang aktif
        gudang = db.query(GudangModel).filter(
            GudangModel.gudang_id == gudang_id,
            GudangModel.gudang_aktif == 'Aktif'
        ).first()
        if not gudang:
            raise ValueError(f"Gudang dengan ID {gudang_id} tidak ditemukan atau tidak aktif.")
        return True
    finally:
        db.close()

def validate_supplier_by_id(supplier_id: int) -> bool:
    """
    Untuk memvalidasi keberadaan supplier berdasarkan ID
    """
    db: Session = SessionLocal()
    try:
        # Query untuk memeriksa keberadaan supplier yang aktif
        supplier = db.query(SupplierModel).filter(
            SupplierModel.supplier_id == supplier_id,
            SupplierModel.supplier_aktif == 'Aktif'
        ).first()
        if not supplier:
            raise ValueError(f"Supplier dengan ID {supplier_id} tidak ditemukan atau tidak aktif.")
        return True
    finally:
        db.close()

def validate_customer_by_id(cust_id: int) -> bool:
    """
    Untuk memvalidasi keberadaan customer berdasarkan ID
    """
    db: Session = SessionLocal()
    try:
        # Query untuk memeriksa keberadaan customer yang aktif
        customer = db.query(CustomerModel).filter(
            CustomerModel.cust_id == cust_id,
            CustomerModel.cust_aktif == 'Aktif'
        ).first()
        if not customer:
            raise ValueError(f"Customer dengan ID {cust_id} tidak ditemukan atau tidak aktif.")
        return True
    finally:
        db.close()

def validate_produk_group_by_id(group_id: int) -> bool:
    """
    Untuk memvalidasi keberadaan produk berdasarkan ID
    """
    db: Session = SessionLocal()
    try:
        # Query untuk memeriksa keberadaan produk_group yang aktif
        produk_group = db.query(ProdukGroupModel).filter(
            ProdukGroupModel.group_id == group_id,
            ProdukGroupModel.group_aktif == 'Aktif'
        ).first()
        if not produk_group:
            raise ValueError(f"Produk Group dengan ID {group_id} tidak ditemukan atau tidak aktif.")
        return True
    finally:
        db.close()

def validate_produk_group_sub_by_id(produk_group: int, produk_group_sub: int) -> bool:
    """
    Untuk memvalidasi keberadaan satuan berdasarkan ID
    """
    db: Session = SessionLocal()
    try:
        # Query untuk memeriksa keberadaan produk_group_sub yang aktif
        cek_produk_group_sub = db.query(ProdukGroupSubModel).filter(
            ProdukGroupSubModel.group_id == produk_group,
            ProdukGroupSubModel.id == produk_group_sub
        ).first()
        if not cek_produk_group_sub:
            raise ValueError(f"Produk Group Sub dengan ID {produk_group_sub} tidak ditemukan pada produk group {produk_group} atau tidak aktif.")
        return True
    finally:
        db.close()

def validate_produk_by_id(produk_id: int) -> bool:
    """
    Untuk memvalidasi keberadaan produk berdasarkan ID
    """
    db: Session = SessionLocal()
    try:
        # Query untuk memeriksa keberadaan produk yang aktif
        produk = db.query(ProdukModel).filter(
            ProdukModel.produk_id == produk_id,
            ProdukModel.produk_aktif == 'Aktif'
        ).first()
        if not produk:
            raise ValueError(f"Produk dengan ID {produk_id} tidak ditemukan atau tidak aktif.")
        return True
    finally:
        db.close()

def validate_satuan_by_id(satuan_id: int) -> bool:
    """
    Untuk memvalidasi keberadaan satuan berdasarkan ID
    """
    db: Session = SessionLocal()
    try:
        # Query untuk memeriksa keberadaan satuan yang aktif
        satuan = db.query(SatuanModel).filter(
            SatuanModel.satuan_id == satuan_id,
            SatuanModel.satuan_aktif == 'Aktif'
        ).first()
        if not satuan:
            raise ValueError(f"Satuan dengan ID {satuan_id} tidak ditemukan atau tidak aktif.")
        return True
    finally:
        db.close()

def validate_satuan_konversi_produk_by_id(produk_id: int, satuan_id: int) -> bool:
    """
    Untuk memvalidasi keberadaan satuan berdasarkan ID
    """
    db: Session = SessionLocal()
    try:
        # Query untuk memeriksa keberadaan satuan yang aktif
        satuan_konversi = db.query(SatuanKonversiModel).filter(
            SatuanKonversiModel.konversi_produk == produk_id,
            SatuanKonversiModel.konversi_satuan == satuan_id
        ).first()
        if not satuan_konversi:
            raise ValueError(f"Satuan dengan ID {satuan_id} tidak ditemukan pada produk {produk_id} atau tidak aktif.")
        return True
    finally:
        db.close()