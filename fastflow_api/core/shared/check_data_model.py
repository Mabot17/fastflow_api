# ============================================= Start Noted Global check ===================================
# Author : Abdul Rohman Masrifan | masrifan26@gamil.com
# 1. Dipakai untuk global check data ada apa tidak, karena akan banyak dipakai di berbagai modul
# ============================================= END Noted Global check ===================================
# Import dependencies python
from sqlalchemy import and_, or_
from sqlalchemy.orm import Session
from typing import Optional

async def check_users(
    db: Session, user_id: int, exclude_id: int = None
):
    from core.modules.users.model.users_model import UsersModel
    filter = []
    filter.append(or_(UsersModel.user_id == user_id))

    if exclude_id:
        filter.append(UsersModel.user_id != user_id)
    criterion = and_(*filter)

    users = db.query(UsersModel).filter(criterion).first()

    return users

async def check_user_by_kode(
    db: Session, user_kode: str, exclude_user_id: int = None
):
    from core.modules.users.model.users_model import UsersModel
    
    filter = []
    filter.append(or_(UsersModel.user_kode == user_kode))

    if exclude_user_id:
        filter.append(UsersModel.id != exclude_user_id)
    criterion = and_(*filter)

    user = db.query(UsersModel).filter(criterion).first()

    return user

async def check_user_by_username(
    db: Session, user_name: str, exclude_user_id: int = None
):
    from core.modules.users.model.users_model import UsersModel
    # Param for_login untuk pengecekan apakah function ini digunakan
    # untuk penambahan/pengubahan data atau ketika user login
    filter = []
    filter.append(or_(UsersModel.user_name == user_name))
    filter.append(UsersModel.deleted_at.is_(None))
    filter.append(UsersModel.deleted_by.is_(None))
    filter.append(UsersModel.user_aktif == "Aktif")

    if exclude_user_id:
        filter.append(UsersModel.id != exclude_user_id)
    criterion = and_(*filter)

    user = db.query(UsersModel).filter(criterion).first()

    return user

async def check_user_by_user_otp_code(
    db: Session, user_otp_code: str, exclude_user_id: int = None
):
    from core.modules.users.model.users_model import UsersModel
    # Param for_login untuk pengecekan apakah function ini digunakan
    # untuk penambahan/pengubahan data atau ketika user login
    filter = []
    filter.append(or_(UsersModel.user_otp_code == user_otp_code))
    filter.append(UsersModel.deleted_at.is_(None))
    filter.append(UsersModel.deleted_by.is_(None))
    filter.append(UsersModel.user_aktif == "Aktif")

    if exclude_user_id:
        filter.append(UsersModel.id != exclude_user_id)
    criterion = and_(*filter)

    user = db.query(UsersModel).filter(criterion).first()

    return user


async def check_customer(
    db: Session, cust_id: int, exclude_cust_id: int = None
):
    from core.modules.customer.model.customer_model import CustomerModel
    
    filter = []
    filter.append(and_(
        CustomerModel.cust_id == cust_id,
        CustomerModel.deleted_at.is_(None),
        CustomerModel.deleted_by.is_(None)
    ))

    if exclude_cust_id:
        filter.append(CustomerModel.cust_id != exclude_cust_id)
    criterion = and_(*filter)

    customer = db.query(CustomerModel).filter(criterion).first()

    return customer

async def check_cust_nama_lengkap(
    db: Session, cust_nama_lengkap: str, exclude_cust_id: int = None
):
    from core.modules.customer.model.customer_model import CustomerModel
    
    filter = []
    filter.append(and_(
        CustomerModel.cust_nama_lengkap == cust_nama_lengkap,
        CustomerModel.deleted_at.is_(None),
        CustomerModel.deleted_by.is_(None)
    ))

    if exclude_cust_id:
        filter.append(CustomerModel.cust_id != exclude_cust_id)
    criterion = and_(*filter)

    customer = db.query(CustomerModel).filter(criterion).first()

    return customer

async def check_cust_no(
    db: Session, cust_no: str, exclude_cust_id: int = None
):
    from core.modules.customer.model.customer_model import CustomerModel
    
    filter = []
    filter.append(and_(
        CustomerModel.cust_no == cust_no,
        CustomerModel.deleted_at.is_(None),
        CustomerModel.deleted_by.is_(None)
    ))

    if exclude_cust_id:
        filter.append(CustomerModel.cust_id != exclude_cust_id)
    criterion = and_(*filter)

    customer = db.query(CustomerModel).filter(criterion).first()

    return customer


async def check_satuan(
    db: Session, satuan_id: int, exclude_satuan_id: int = None
):
    from core.modules.satuan.model.satuan_model import SatuanModel
    
    filter = []
    filter.append(and_(
        SatuanModel.satuan_id == satuan_id,
        SatuanModel.deleted_at.is_(None),
        SatuanModel.deleted_by.is_(None)
    ))

    if exclude_satuan_id:
        filter.append(SatuanModel.satuan_id != exclude_satuan_id)
    criterion = and_(*filter)

    satuan = db.query(SatuanModel).filter(criterion).first()

    return satuan

async def check_satuan_kode(
    db: Session, satuan_kode: int, exclude_satuan_id: int = None
):
    from core.modules.satuan.model.satuan_model import SatuanModel
    
    filter = []
    filter.append(and_(
        SatuanModel.satuan_kode == satuan_kode,
        SatuanModel.deleted_at.is_(None),
        SatuanModel.deleted_by.is_(None)
    ))

    if exclude_satuan_id:
        filter.append(SatuanModel.satuan_id != exclude_satuan_id)
    criterion = and_(*filter)

    satuan = db.query(SatuanModel).filter(criterion).first()

    return satuan

async def check_produk_group(
    db: Session, group_id: int, exclude_group_id: int = None
):
    from core.modules.produk_group.model.produk_group_model import ProdukGroupModel
    
    filter = []
    filter.append(and_(
        ProdukGroupModel.group_id == group_id,
        ProdukGroupModel.deleted_at.is_(None),
        ProdukGroupModel.deleted_by.is_(None)
    ))

    if exclude_group_id:
        filter.append(ProdukGroupModel.group_id != exclude_group_id)
    criterion = and_(*filter)

    produk_group = db.query(ProdukGroupModel).filter(criterion).first()

    return produk_group

async def check_group_kode(
    db: Session, group_kode: int, exclude_group_id: int = None
):
    from core.modules.produk_group.model.produk_group_model import ProdukGroupModel
    
    filter = []
    filter.append(and_(
        ProdukGroupModel.group_kode == group_kode,
        ProdukGroupModel.deleted_at.is_(None),
        ProdukGroupModel.deleted_by.is_(None)
    ))

    if exclude_group_id:
        filter.append(ProdukGroupModel.group_id != exclude_group_id)
    criterion = and_(*filter)

    produk_group = db.query(ProdukGroupModel).filter(criterion).first()

    return produk_group


async def check_produk(
    db: Session, produk_id: int, exclude_produk_id: int = None
):
    from core.modules.produk.model.produk_model import ProdukModel
    
    filter = []
    filter.append(and_(
        ProdukModel.produk_id == produk_id,
        ProdukModel.deleted_at.is_(None),
        ProdukModel.deleted_by.is_(None)
    ))

    if exclude_produk_id:
        filter.append(ProdukModel.produk_id != exclude_produk_id)
    criterion = and_(*filter)

    produk = db.query(ProdukModel).filter(criterion).first()

    return produk

async def check_produk_nama(
    db: Session, produk_nama: str, exclude_produk_id: int = None
):
    from core.modules.produk.model.produk_model import ProdukModel
    
    filter = []
    filter.append(and_(
        ProdukModel.produk_nama == produk_nama,
        ProdukModel.deleted_at.is_(None),
        ProdukModel.deleted_by.is_(None)
    ))

    if exclude_produk_id:
        filter.append(ProdukModel.produk_id != exclude_produk_id)
    criterion = and_(*filter)

    produk = db.query(ProdukModel).filter(criterion).first()

    return produk

async def check_produk_kode(
    db: Session, produk_kode: int, exclude_produk_id: int = None
):
    from core.modules.produk.model.produk_model import ProdukModel
    
    filter = []
    filter.append(and_(
        ProdukModel.produk_kode == produk_kode,
        ProdukModel.deleted_at.is_(None),
        ProdukModel.deleted_by.is_(None)
    ))

    if exclude_produk_id:
        filter.append(ProdukModel.produk_id != exclude_produk_id)
    criterion = and_(*filter)

    produk = db.query(ProdukModel).filter(criterion).first()

    return produk


async def check_produk_satuan_konversi(
    db: Session, produk_id : int, satuan_id: int, exclude_konversi_id: int = None
):
    from core.modules.produk.model.satuan_konversi_model import SatuanKonversiModel
    
    filter = []
    filter.append(and_(
        SatuanKonversiModel.konversi_produk == produk_id,
        SatuanKonversiModel.konversi_satuan == satuan_id,
        SatuanKonversiModel.deleted_at.is_(None),
        SatuanKonversiModel.deleted_by.is_(None)
    ))

    if exclude_konversi_id:
        filter.append(SatuanKonversiModel.konversi_id != exclude_konversi_id)
    criterion = and_(*filter)

    satuan_konversi = db.query(SatuanKonversiModel).filter(criterion).first()

    return satuan_konversi

async def check_satuan_konversi(
    db: Session, produk_id : int, konversi_id: int, exclude_konversi_id: int = None
):
    from core.modules.produk.model.satuan_konversi_model import SatuanKonversiModel
    
    filter = []
    filter.append(and_(
        SatuanKonversiModel.konversi_produk == produk_id,
        SatuanKonversiModel.konversi_id == konversi_id,
        SatuanKonversiModel.deleted_at.is_(None),
        SatuanKonversiModel.deleted_by.is_(None)
    ))

    if exclude_konversi_id:
        filter.append(SatuanKonversiModel.konversi_id != exclude_konversi_id)
    criterion = and_(*filter)

    satuan_konversi = db.query(SatuanKonversiModel).filter(criterion).first()

    return satuan_konversi


async def check_master_jual_produk(
    db: Session, jproduk_id: int, exclude_jproduk_id: int = None
):
    from core.modules.master_jual_produk.model.master_jual_produk_model import MasterJualProdukModel
    
    filter = []
    filter.append(and_(
        MasterJualProdukModel.jproduk_id == jproduk_id,
        MasterJualProdukModel.deleted_by.is_(None)
    ))

    if exclude_jproduk_id:
        filter.append(MasterJualProdukModel.jproduk_id != exclude_jproduk_id)
    criterion = and_(*filter)

    master_jual_produk = db.query(MasterJualProdukModel).filter(criterion).first()

    return master_jual_produk

async def check_detail_jual_produk(
    db: Session, dproduk_id: int, jproduk_id : int = None, exclude_dproduk_id: int = None
):
    from core.modules.master_jual_produk.model.master_jual_produk_model import DetailJualProdukModel
    
    filter = []
    filter.append(and_(
        DetailJualProdukModel.dproduk_id == dproduk_id,
        DetailJualProdukModel.deleted_at.is_(None),
        DetailJualProdukModel.deleted_by.is_(None)
    ))

    if jproduk_id:
        filter.append(DetailJualProdukModel.dproduk_master == jproduk_id)

    if exclude_dproduk_id:
        filter.append(DetailJualProdukModel.dproduk_id != exclude_dproduk_id)
    criterion = and_(*filter)

    detail_jual_produk = db.query(DetailJualProdukModel).filter(criterion).first()

    return detail_jual_produk