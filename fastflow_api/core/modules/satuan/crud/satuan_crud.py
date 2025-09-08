# ============================================= Start Noted CRUD ===================================
# Author : PT. Dapur Perangkat Lunak Indonesia | KoffieSoft Group | https://www.koffiesoft.com/ | info@koffiesoft.com
# 1. Response return wajib JSON/dict supaya bisa diolah kembali di router
# ============================================= END Noted CRUD ===================================
from sqlalchemy.orm import Session, aliased
from sqlalchemy import and_, func, or_
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from core.modules.satuan.model.satuan_model import SatuanModel
from core.utils.common import SUCCESS, total_pages, start_from
from core.modules.satuan.schema.satuan_schema import SatuanBaseDataSchema, SatuanReqSchema, SatuanPutSchema, SatuanRequestListSchema
from core.modules.users.schema.users_schema import UsersBaseSchema
from datetime import datetime
from typing import List, Optional, Dict

from core.shared.check_data_model import (
    check_satuan,
)

from core.shared.json_helpers.json_satuan import json_satuan

import logging

async def get_crud_daftar_satuan(db: Session, request: SatuanRequestListSchema) -> List:
    try:
        satuanModel = aliased(SatuanModel, name="satuanModel")

        query = db.query(satuanModel)
        if request.keywords and request.keywords.strip():
            keywords_lower = request.keywords.lower()
            query = query.filter(
                or_(
                    func.lower(satuanModel.satuan_kode).like(f"%{keywords_lower}%"),
                    func.lower(satuanModel.satuan_nama).like(f"%{keywords_lower}%"),
                    func.lower(satuanModel.satuan_keterangan).like(f"%{keywords_lower}%")
                )
            )

        filter = []

        # Filter belum pernah dihapus
        filter.append(satuanModel.deleted_at.is_(None))
        filter.append(satuanModel.deleted_by.is_(None))

        # Filter berdasarkan satuan_aktif
        if request.satuan_aktif is not None:
            if request.satuan_aktif == 'Aktif':
                filter.append(satuanModel.satuan_aktif == 'Aktif')
            elif request.satuan_aktif == 'Tidak Aktif':
                filter.append(satuanModel.satuan_aktif == 'Tidak Aktif')
        
        # Gabungkan semua filter menggunakan operator AND
        query = query.filter(and_(*filter))

        qr_count = query.count()
        count = qr_count

        qr_data = (
            query.order_by(satuanModel.satuan_id.desc())
            .limit(request.results_per_page)
            .offset(start_from(request.page, request.results_per_page))
            .all()
        )

        result_data = [
            await json_satuan(db=db, satuan_data_row=row, timestamp_data=request.timestamp_data)
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

async def select_satuan_by_id(
    db: Session,
    satuan_id: int,
    timestamp_data: bool = False
) -> Dict:
    try:
        result = (
            db.query(SatuanModel)
            .filter(
                and_(
                    SatuanModel.satuan_id == satuan_id,
                    SatuanModel.deleted_at.is_(None),
                    SatuanModel.deleted_by.is_(None),
                )
            )
            .first()
        )

        if result:
            return await json_satuan(
                db=db,
                satuan_data_row=result,
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


async def create_data_satuan(db: Session, satuan_data_create: SatuanReqSchema, identity: UsersBaseSchema):
    new_satuan = SatuanModel()
    try:
        new_satuan.satuan_kode = satuan_data_create.satuan_kode
        new_satuan.satuan_nama = satuan_data_create.satuan_nama
        new_satuan.satuan_aktif = satuan_data_create.satuan_aktif
        new_satuan.satuan_keterangan = satuan_data_create.satuan_keterangan

        new_satuan.created_at = datetime.now()
        new_satuan.created_by = identity.user_name

        db.add(new_satuan)
        db.commit()
        db.refresh(new_satuan)

        return await json_satuan(
            db=db,
            satuan_data_row=new_satuan
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

async def update_data_satuan(db: Session, satuan_id: int, satuan_data_update: SatuanPutSchema, identity: UsersBaseSchema):
    try:
        old_satuan = await check_satuan(db, satuan_id=satuan_id)
        if old_satuan:
            old_satuan.satuan_kode = satuan_data_update.satuan_kode
            old_satuan.satuan_nama = satuan_data_update.satuan_nama
            old_satuan.satuan_aktif = satuan_data_update.satuan_aktif
            old_satuan.satuan_keterangan = satuan_data_update.satuan_keterangan

            # Update data flag
            old_satuan.revised = (old_satuan.revised or 0) + 1
            old_satuan.updated_by = identity.user_name
            old_satuan.updated_at = datetime.now()

            db.commit()
            db.refresh(old_satuan)


            return await json_satuan(
                db=db,
                satuan_data_row=old_satuan
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
async def partial_update_data_satuan(db: Session, satuan_id: int, satuan_data_update: dict, identity: UsersBaseSchema):
    try:
        old_patch_satuan = await check_satuan(db, satuan_id=satuan_id)
        if old_patch_satuan:
            # Update fields only if they are present in the provided data
            for field, value in satuan_data_update.items():
                if hasattr(old_patch_satuan, field):
                    setattr(old_patch_satuan, field, value)

            # Update data flag
            old_patch_satuan.revised = (old_patch_satuan.revised or 0) + 1
            old_patch_satuan.updated_by = identity.user_name
            old_patch_satuan.updated_at = datetime.now()

            db.commit()
            db.refresh(old_patch_satuan)

            return await json_satuan(
                db=db,
                satuan_data_row=old_patch_satuan
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
    
async def delete_data_satuan(db: Session, satuan_id: int, identity: UsersBaseSchema):
    deleted_satuan = await check_satuan(db, satuan_id=satuan_id)
    try:
        deleted_satuan.satuan_aktif = 'Tidak Aktif'
        deleted_satuan.deleted_by = identity.user_name
        deleted_satuan.deleted_at = datetime.now()

        db.commit()
        db.refresh(deleted_satuan)

        return await json_satuan(
            db=db,
            satuan_data_row=deleted_satuan
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