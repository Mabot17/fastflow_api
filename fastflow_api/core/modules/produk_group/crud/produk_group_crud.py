# ============================================= Start Noted CRUD ===================================
# Author : PT. Dapur Perangkat Lunak Indonesia | KoffieSoft Group | https://www.koffiesoft.com/ | info@koffiesoft.com
# 1. Response return wajib JSON/dict supaya bisa diolah kembali di router
# ============================================= END Noted CRUD ===================================
from sqlalchemy.orm import Session, aliased
from sqlalchemy import and_, func, or_
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from core.modules.produk_group.model.produk_group_model import ProdukGroupModel
from core.utils.common import SUCCESS, total_pages, start_from
from core.modules.produk_group.schema.produk_group_schema import ProdukGroupBaseDataSchema, ProdukGroupReqSchema, ProdukGroupPutSchema, ProdukGroupRequestListSchema
from core.modules.users.schema.users_schema import UsersBaseSchema
from datetime import datetime
from typing import List, Optional, Dict

from core.shared.check_data_model import (
    check_produk_group,
)

from core.shared.json_helpers.json_produk_group import json_produk_group

import logging

async def get_crud_daftar_produk_group(db: Session, request: ProdukGroupRequestListSchema) -> List:
    try:
        produk_groupModel = aliased(ProdukGroupModel, name="produk_groupModel")

        query = db.query(produk_groupModel)
        if request.keywords and request.keywords.strip():
            keywords_lower = request.keywords.lower()
            query = query.filter(
                or_(
                    func.lower(produk_groupModel.group_kode).like(f"%{keywords_lower}%"),
                    func.lower(produk_groupModel.group_nama).like(f"%{keywords_lower}%"),
                    func.lower(produk_groupModel.group_keterangan).like(f"%{keywords_lower}%")
                )
            )

        filter = []

        # Filter belum pernah dihapus
        filter.append(produk_groupModel.deleted_at.is_(None))
        filter.append(produk_groupModel.deleted_by.is_(None))

        # Filter berdasarkan group_aktif
        if request.group_aktif is not None:
            if request.group_aktif == 'Aktif':
                filter.append(produk_groupModel.group_aktif == 'Aktif')
            elif request.group_aktif == 'Tidak Aktif':
                filter.append(produk_groupModel.group_aktif == 'Tidak Aktif')
        
        # Gabungkan semua filter menggunakan operator AND
        query = query.filter(and_(*filter))

        qr_count = query.count()
        count = qr_count

        qr_data = (
            query.order_by(produk_groupModel.group_id.desc())
            .limit(request.results_per_page)
            .offset(start_from(request.page, request.results_per_page))
            .all()
        )

        result_data = [
            await json_produk_group(db=db, produk_group_data_row=row, timestamp_data=request.timestamp_data)
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

async def select_produk_group_by_id(
    db: Session,
    group_id: int,
    timestamp_data: bool = False
) -> Dict:
    try:
        result = (
            db.query(ProdukGroupModel)
            .filter(
                and_(
                    ProdukGroupModel.group_id == group_id,
                    ProdukGroupModel.deleted_at.is_(None),
                    ProdukGroupModel.deleted_by.is_(None),
                )
            )
            .first()
        )

        if result:
            return await json_produk_group(
                db=db,
                produk_group_data_row=result,
                timestamp_data=timestamp_data
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


async def create_data_produk_group(db: Session, produk_group_data_create: ProdukGroupReqSchema, identity: UsersBaseSchema):
    new_produk_group = ProdukGroupModel()
    try:
        new_produk_group.group_kode = produk_group_data_create.group_kode
        new_produk_group.group_nama = produk_group_data_create.group_nama
        new_produk_group.group_aktif = produk_group_data_create.group_aktif
        new_produk_group.group_keterangan = produk_group_data_create.group_keterangan

        new_produk_group.created_at = datetime.now()
        new_produk_group.created_by = identity.user_name

        db.add(new_produk_group)
        db.commit()
        db.refresh(new_produk_group)

        return await json_produk_group(
            db=db,
            produk_group_data_row=new_produk_group
        )
    except IntegrityError as e:
        logging.error(f"IntegrityError: {e}")
        return None  # Tangani kesalahan unik di endpoint
    except SQLAlchemyError as e:
        logging.error(f"SQLAlchemyError: {e}")
        return None
    except Exception as e:
        logging.error(e)
        return e

async def update_data_produk_group(db: Session, group_id: int, produk_group_data_update: ProdukGroupPutSchema, identity: UsersBaseSchema):
    try:
        old_produk_group = await check_produk_group(db, group_id=group_id)
        if old_produk_group:
            old_produk_group.group_kode = produk_group_data_update.group_kode
            old_produk_group.group_nama = produk_group_data_update.group_nama
            old_produk_group.group_aktif = produk_group_data_update.group_aktif
            old_produk_group.group_keterangan = produk_group_data_update.group_keterangan

            # Update data flag
            old_produk_group.revised = (old_produk_group.revised or 0) + 1
            old_produk_group.updated_by = identity.user_name
            old_produk_group.updated_at = datetime.now()

            db.commit()
            db.refresh(old_produk_group)


            return await json_produk_group(
                db=db,
                produk_group_data_row=old_produk_group
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
        logging.error(e)
        return None
    
  
# Update method patch, jadi bisa diupdate salah satu kolom / bbrp kolom saja. tanpa pengecekan required dahulu
async def partial_update_data_produk_group(db: Session, group_id: int, produk_group_data_update: dict, identity: UsersBaseSchema):
    try:
        old_patch_produk_group = await check_produk_group(db, group_id=group_id)
        if old_patch_produk_group:
            # Update fields only if they are present in the provided data
            for field, value in produk_group_data_update.items():
                if hasattr(old_patch_produk_group, field):
                    setattr(old_patch_produk_group, field, value)

            # Update data flag
            old_patch_produk_group.revised = (old_patch_produk_group.revised or 0) + 1
            old_patch_produk_group.updated_by = identity.user_name
            old_patch_produk_group.updated_at = datetime.now()

            db.commit()
            db.refresh(old_patch_produk_group)

            return await json_produk_group(
                db=db,
                produk_group_data_row=old_patch_produk_group
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
    
async def delete_data_produk_group(db: Session, group_id: int, identity: UsersBaseSchema):
    deleted_produk_group = await check_produk_group(db, group_id=group_id)
    try:
        deleted_produk_group.group_aktif = 'Tidak Aktif'
        deleted_produk_group.deleted_by = identity.user_name
        deleted_produk_group.deleted_at = datetime.now()

        db.commit()
        db.refresh(deleted_produk_group)

        return await json_produk_group(
            db=db,
            produk_group_data_row=deleted_produk_group
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