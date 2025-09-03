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


async def check_usergroups(
    db: Session, group_id: int, exclude_usergroups_id: int = None
):
    from core.modules.usergroups.model.usergroups_model import UsergroupsModel
    filter = []
    filter.append(or_(UsergroupsModel.group_id == group_id))

    if exclude_usergroups_id:
        filter.append(UsergroupsModel.group_id != exclude_usergroups_id)
    criterion = and_(*filter)

    usergroups = db.query(UsergroupsModel).filter(criterion).first()

    return usergroups

async def check_usergroups_name(
    db: Session, group_name: str, exclude_group_id: int = None
):
    from core.modules.usergroups.model.usergroups_model import UsergroupsModel
    
    filter = []
    filter.append(and_(
        UsergroupsModel.group_name == group_name,
        UsergroupsModel.deleted_at.is_(None),
        UsergroupsModel.deleted_by.is_(None)
    ))

    if exclude_group_id:
        filter.append(UsergroupsModel.group_id != exclude_group_id)
    criterion = and_(*filter)

    usergroups_name = db.query(UsergroupsModel).filter(criterion).first()

    return usergroups_name

async def check_produk_barcode(
    db: Session, productId: int, exclude_productId: int = None
):
    from core.modules.master.produk_barcode.model.produk_barcode_model import ProdukBarcodeModel
    filter = []
    filter.append(and_(
        ProdukBarcodeModel.productId == productId,
        ProdukBarcodeModel.deleted_at.is_(None),
        ProdukBarcodeModel.deleted_by.is_(None)
    ))

    if exclude_productId:
        filter.append(ProdukBarcodeModel.productId != exclude_productId)
    criterion = and_(*filter)

    produk_barcode = db.query(ProdukBarcodeModel).filter(criterion).first()

    return produk_barcode

async def check_product_by_barcode(
    db: Session, productBarcode: str, exclude_productId: int = None
):
    from core.modules.master.produk_barcode.model.produk_barcode_model import ProdukBarcodeModel
    filter = []
    filter.append(and_(
        ProdukBarcodeModel.productBarcode == productBarcode,
        ProdukBarcodeModel.deleted_at.is_(None),
        ProdukBarcodeModel.deleted_by.is_(None)
    ))

    if exclude_productId:
        filter.append(ProdukBarcodeModel.productId != exclude_productId)
    criterion = and_(*filter)

    produk_barcode = db.query(ProdukBarcodeModel).filter(criterion).first()

    return produk_barcode

async def check_produk_barcode_kategori(
    db: Session, categoryId: str, exclude_categoryId: int = None
):
    from core.modules.master.produk_barcode_kategori.model.produk_barcode_kategori_model import ProdukBarcodeKategoriModel
    filter = []
    filter.append(and_(
        ProdukBarcodeKategoriModel.categoryId == categoryId,
        ProdukBarcodeKategoriModel.deleted_at.is_(None),
        ProdukBarcodeKategoriModel.deleted_by.is_(None)
    ))

    if exclude_categoryId:
        filter.append(ProdukBarcodeKategoriModel.categoryId != exclude_categoryId)
    criterion = and_(*filter)

    produk_barcode_kategori = db.query(ProdukBarcodeKategoriModel).filter(criterion).first()

    return produk_barcode_kategori

async def check_produk_digital(
    db: Session, produk_digital_id: int, exclude_produk_digital_id: int = None
):
    from core.modules.master.produk_digital.model.produk_digital_model import ProdukDigitalModel
    filter = []
    filter.append(and_(
        ProdukDigitalModel.produk_digital_id == produk_digital_id,
        ProdukDigitalModel.deleted_at.is_(None),
        ProdukDigitalModel.deleted_by.is_(None)
    ))

    if exclude_produk_digital_id:
        filter.append(ProdukDigitalModel.produk_digital_id != exclude_produk_digital_id)
    criterion = and_(*filter)

    produk_digital = db.query(ProdukDigitalModel).filter(criterion).first()

    return produk_digital

async def check_produk_digital_by_kode(
    db: Session, produk_digital_kode: str, exclude_produk_digital_id: int = None
):
    from core.modules.master.produk_digital.model.produk_digital_model import ProdukDigitalModel
    filter = []
    filter.append(and_(
        ProdukDigitalModel.produk_digital_kode == produk_digital_kode,
        ProdukDigitalModel.deleted_at.is_(None),
        ProdukDigitalModel.deleted_by.is_(None)
    ))

    if exclude_produk_digital_id:
        filter.append(ProdukDigitalModel.produk_digital_id != exclude_produk_digital_id)
    criterion = and_(*filter)

    produk_digital = db.query(ProdukDigitalModel).filter(criterion).first()

    return produk_digital

async def check_produk_users(
    db: Session, users_id: int, productId: int, exclude_productId: int = None
):
    from core.modules.master.produk_users.model.produk_users_model import ProdukUsersModel
    filter = []
    filter.append(and_(
        ProdukUsersModel.user_id == users_id,
        ProdukUsersModel.produk_header_id == productId,
        ProdukUsersModel.deleted_at.is_(None),
        ProdukUsersModel.deleted_by.is_(None)
    ))

    if exclude_productId:
        filter.append(ProdukUsersModel.produk_header_id != exclude_productId)
    criterion = and_(*filter)

    produk_users = db.query(ProdukUsersModel).filter(criterion).first()

    return produk_users

async def check_chat(
    db: Session, chat_id: int, exclude_chat_id: int = None
):
    from core.modules.socket_chat.model.chat_model import ChatMessages
    
    filter = []
    filter.append(and_(
        ChatMessages.id == chat_id,
        ChatMessages.deleted_at.is_(None)
    ))

    if exclude_chat_id:
        filter.append(ChatMessages.id != exclude_chat_id)
    criterion = and_(*filter)

    chat = db.query(ChatMessages).filter(criterion).first()

    return chat

async def check_project_chat(
    db: Session, id: int, exclude_id: int = None
):
    from core.modules.socket_chat.model.chat_model import ProjectChatMessagesModel
    
    filter = []
    filter.append(and_(
        ProjectChatMessagesModel.id == id,
        ProjectChatMessagesModel.deleted_at.is_(None),
    ))

    if exclude_id:
        filter.append(ProjectChatMessagesModel.id != exclude_id)
    criterion = and_(*filter)

    project_chat = db.query(ProjectChatMessagesModel).filter(criterion).first()

    return project_chat