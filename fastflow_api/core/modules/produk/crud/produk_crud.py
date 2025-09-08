# ============================================= Start Noted CRUD ===================================
# Author : PT. Dapur Perangkat Lunak Indonesia | KoffieSoft Group | https://www.koffiesoft.com/ | info@koffiesoft.com
# 1. Response return wajib JSON/dict supaya bisa diolah kembali di router
# ============================================= END Noted CRUD ===================================
from sqlalchemy.orm import Session, aliased
from sqlalchemy import and_, func, or_
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from datetime import datetime
from typing import List, Optional, Dict

# Import models core
from core.modules.produk.model.produk_model import ProdukModel
from core.modules.produk.schema.produk_schema import ProdukBaseDataSchema, ProdukReqSchema, ProdukPutSchema, ProdukRequestListSchema
from core.modules.users.schema.users_schema import UsersBaseSchema
from core.utils.common import SUCCESS, total_pages, start_from
from core.utils.generate_no_faktur import generate_produk_kode

from core.shared.check_data_model import (
    check_produk,
)

from core.shared.json_helpers.json_produk import json_produk

import logging

async def get_crud_daftar_produk(db: Session, request: ProdukRequestListSchema) -> List:
    try:
        produkModel = aliased(ProdukModel, name="produkModel")

        query = db.query(produkModel)
        if request.keywords and request.keywords.strip():
            keywords_lower = request.keywords.lower()
            query = query.filter(
                or_(
                    func.lower(produkModel.produk_kode).like(f"%{keywords_lower}%"),
                    func.lower(produkModel.produk_sku).like(f"%{keywords_lower}%"),
                    func.lower(produkModel.produk_nama).like(f"%{keywords_lower}%"),
                    func.lower(produkModel.produk_keterangan).like(f"%{keywords_lower}%")
                )
            )

        filter = []

        # Filter belum pernah dihapus
        filter.append(
            or_(
                produkModel.deleted_at.is_(None),
            )
        )
        filter.append(
            or_(
                produkModel.deleted_by.is_(None),
            )
        )

        # Filter berdasarkan produk_aktif
        if request.produk_aktif is not None and request.produk_aktif != 'Semua' :
            filter.append(produkModel.produk_aktif == request.produk_aktif)

        # Filter berdasarkan produk_group
        if request.produk_group is not None:
            filter.append(produkModel.produk_group == request.produk_group)

        # Filter berdasarkan produk_sku
        if request.produk_sku is not None:
            filter.append(produkModel.produk_sku == request.produk_sku)
        
        # Gabungkan semua filter menggunakan operator AND
        query = query.filter(and_(*filter))

        qr_count = query.count()
        count = qr_count

        qr_data = (
            query.order_by(produkModel.produk_id.desc())
            .limit(request.results_per_page)
            .offset(start_from(request.page, request.results_per_page))
            .all()
        )

        result_data = [
            await json_produk(
                db=db,
                produk_data_row=row,
                timestamp_data=request.timestamp_data,
                produk_satuan_konversi_data=request.produk_satuan_konversi_data,
                produk_group_data=request.produk_group_data,
            )
            for row in qr_data
        ]

        if result_data:  # Check if result_data is not an empty list
            return {"data": result_data, "total_data" : count}
        else:
            return {"data": None, "total_data" : 0}
    
    except IntegrityError as e:
        logging.error(f"IntegrityError: {e}")
        return {"data": None, "total_data" : 0}
    except SQLAlchemyError as e:
        logging.error(f"SQLAlchemyError: {e}")
        return {"data": None, "total_data": 0}
    except Exception as e:
        logging.error(e)
        return {"data": None, "total_data" : 0}

async def select_produk_by_id(
    db: Session,
    produk_id: int,
    timestamp_data: bool = False
) -> Dict:
    try:
        result = (
            db.query(ProdukModel)
            .filter(
                and_(
                    ProdukModel.produk_id == produk_id,
                    ProdukModel.deleted_at.is_(None),
                    ProdukModel.deleted_by.is_(None),
                )
            )
            .first()
        )

        if result:
            return await json_produk(
                db=db,
                produk_data_row=result,
                timestamp_data=timestamp_data,
                produk_satuan_konversi_data=True,
                produk_group_data=True,
            )
        else:
            return None
    except IntegrityError as e:
        logging.error(f"IntegrityError: {e}")
        return None
    except SQLAlchemyError as e:
        logging.error(f"SQLAlchemyError: {e}")
        return None
    except Exception as e:
        logging.error(e)
        return None

async def create_data_produk(
    db: Session,
    produk_data_create: ProdukReqSchema,
    identity: UsersBaseSchema
):
    new_produk = ProdukModel()
    try:
        # Generate kode produk jika tidak diberikan
        new_produk.produk_kode = await generate_produk_kode(
            db=db,
            produk_group=produk_data_create.produk_group
        )

        new_produk.produk_nama       = produk_data_create.produk_nama
        new_produk.produk_sku        = produk_data_create.produk_sku
        new_produk.produk_group      = produk_data_create.produk_group
        new_produk.produk_satuan     = produk_data_create.produk_satuan
        new_produk.produk_harga      = produk_data_create.produk_harga
        new_produk.produk_diskon     = produk_data_create.produk_diskon
        new_produk.produk_diskon_rp  = produk_data_create.produk_diskon_rp
        new_produk.produk_aktif      = produk_data_create.produk_aktif
        new_produk.produk_keterangan = produk_data_create.produk_keterangan

        # Audit field
        new_produk.created_at = datetime.now()
        new_produk.created_by = identity.user_name

        db.add(new_produk)
        db.commit()
        db.refresh(new_produk)

        return await json_produk(
            db=db,
            produk_data_row=new_produk,
            produk_group_data=True,
            timestamp_data=True
        )

    except IntegrityError as e:
        logging.error(f"IntegrityError: {e}")
        db.rollback()
        return None
    except SQLAlchemyError as e:
        logging.error(f"SQLAlchemyError: {e}")
        db.rollback()
        return None
    except Exception as e:
        logging.error(e)
        db.rollback()
        return None


async def update_data_produk(
    db: Session,
    produk_id: int,
    produk_data_update: ProdukPutSchema,
    identity: UsersBaseSchema
):
    try:
        old_produk = await check_produk(db, produk_id=produk_id)
        if not old_produk:
            return None

        # Jika kode produk berubah / kosong → generate ulang
        if produk_data_update.produk_group != old_produk.produk_group:
            old_produk.produk_kode = await generate_produk_kode(
                db=db,
                produk_group=produk_data_update.produk_group
            )

        old_produk.produk_nama       = produk_data_update.produk_nama
        old_produk.produk_sku        = produk_data_update.produk_sku
        old_produk.produk_group      = produk_data_update.produk_group
        old_produk.produk_satuan     = produk_data_update.produk_satuan
        old_produk.produk_harga      = produk_data_update.produk_harga
        old_produk.produk_diskon     = produk_data_update.produk_diskon
        old_produk.produk_diskon_rp  = produk_data_update.produk_diskon_rp
        old_produk.produk_aktif      = produk_data_update.produk_aktif
        old_produk.produk_keterangan = produk_data_update.produk_keterangan

        # Audit update
        old_produk.revised = (old_produk.revised or 0) + 1
        old_produk.updated_by = identity.user_name
        old_produk.updated_at = datetime.now()

        db.commit()
        db.refresh(old_produk)

        return await json_produk(
            db=db,
            produk_data_row=old_produk,
            produk_group_data=True,
            timestamp_data=True
        )

    except IntegrityError as e:
        logging.error(f"IntegrityError: {e}")
        db.rollback()
        return None
    except SQLAlchemyError as e:
        logging.error(f"SQLAlchemyError: {e}")
        db.rollback()
        return None
    except Exception as e:
        logging.error(e)
        db.rollback()
        return None

    
  
# Update method patch, jadi bisa diupdate salah satu kolom / bbrp kolom saja. tanpa pengecekan required dahulu
async def partial_update_data_produk(db: Session, produk_id: int, produk_data_update: dict, identity: UsersBaseSchema):
    try:
        old_patch_produk = await check_produk(db, produk_id=produk_id)
        if old_patch_produk:
            # Update fields only if they are present in the provided data
            for field, value in produk_data_update.items():
                if hasattr(old_patch_produk, field):
                    setattr(old_patch_produk, field, value)

            # Update data flag
            old_patch_produk.revised = (old_patch_produk.revised or 0) + 1
            old_patch_produk.updated_by = identity.user_name
            old_patch_produk.updated_at = datetime.now()

            db.commit()
            db.refresh(old_patch_produk)

            return await json_produk(
                db=db,
                produk_data_row=old_patch_produk,
                produk_group_data=True,
            )
        else:
            return None
    except IntegrityError as e:
        logging.error(f"IntegrityError: {e}")
        return None  # Tangani kesalahan unik di endpoint
    except SQLAlchemyError as e:
        logging.error(f"SQLAlchemyError: {e}")
        return None
    except Exception as e:
        logging.error(f"Exception: {e}")
        return None
    
async def delete_data_produk(db: Session, produk_id: int, identity: UsersBaseSchema):
    deleted_produk = await check_produk(db, produk_id=produk_id)
    try:
        deleted_produk.produk_aktif = 'Tidak Aktif'
        deleted_produk.deleted_by = identity.user_name
        deleted_produk.deleted_at = datetime.now()

        db.commit()
        db.refresh(deleted_produk)

        return await json_produk(
            db=db,
            produk_data_row=deleted_produk,
            produk_group_data=True,
        )
    except IntegrityError as e:
        logging.error(f"IntegrityError: {e}")
        return None  # Tangani kesalahan unik di endpoint
    except SQLAlchemyError as e:
        logging.error(f"SQLAlchemyError: {e}")
        return None
    except Exception as e:
        logging.error(e)
        return None