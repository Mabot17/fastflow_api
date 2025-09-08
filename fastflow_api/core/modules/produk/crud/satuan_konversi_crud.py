# ============================================= Start Noted CRUD ===================================
# Author : PT. Dapur Perangkat Lunak Indonesia | KoffieSoft Group | https://www.koffiesoft.com/ | info@koffiesoft.com
# 1. Response return wajib JSON/dict supaya bisa diolah kembali di router
# ============================================= END Noted CRUD ===================================
from sqlalchemy.orm import Session, aliased
from sqlalchemy import and_, func, or_
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from core.modules.produk.model.satuan_konversi_model import SatuanKonversiModel
from core.utils.common import SUCCESS, total_pages, start_from
from core.modules.produk.schema.satuan_konversi_schema import SatuanKonversiBaseDataSchema, SatuanKonversiReqSchema, SatuanKonversiRequestListSchema
from core.modules.users.schema.users_schema import UsersBaseSchema
from datetime import datetime
from typing import List, Optional, Dict

from core.shared.check_data_model import (
    check_satuan_konversi,
)

from core.shared.json_helpers.json_satuan_konversi import json_satuan_konversi

import logging

async def get_crud_daftar_satuan_konversi(db: Session, produk_id : int, request: SatuanKonversiRequestListSchema) -> List:
    try:
        satuan_konversi_model = aliased(SatuanKonversiModel, name="satuan_konversi_model")

        query = db.query(satuan_konversi_model)
        if request.keywords and request.keywords.strip():
            keywords_lower = request.keywords.lower()
            query = query.filter(
                or_(
                    func.lower(satuan_konversi_model.konversi_satuan).like(f"%{keywords_lower}%"),
                    func.lower(satuan_konversi_model.konversi_keterangan).like(f"%{keywords_lower}%")
                )
            )

        filter = []

        # Filter berdasarkan konversi_aktif
        if request.konversi_aktif is not None:
            if request.konversi_aktif == 'Aktif':
                filter.append(satuan_konversi_model.konversi_aktif == 'Aktif')
            elif request.konversi_aktif == 'Tidak Aktif':
                filter.append(satuan_konversi_model.konversi_aktif == 'Tidak Aktif')

        if produk_id:
            filter.append(satuan_konversi_model.konversi_produk == produk_id)
        
        # Gabungkan semua filter menggunakan operator AND
        query = query.filter(and_(*filter))

        qr_count = query.count()
        count = qr_count

        qr_data = (
            query.order_by(satuan_konversi_model.konversi_id)
            .limit(request.results_per_page)
            .offset(start_from(request.page, request.results_per_page))
            .all()
        )

        result_data = [
            await json_satuan_konversi(db=db, satuan_konversi_data_row=row, timestamp_data=request.timestamp_data, konversi_satuan_data=request.konversi_satuan_data)
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

async def select_satuan_konversi_by_id(
    db: Session,
    produk_id: int,
    konversi_id: int,
    timestamp_data: bool = False
) -> Dict:
    try:
        result = (
            db.query(SatuanKonversiModel)
            .filter(
                and_(
                    SatuanKonversiModel.konversi_produk == produk_id,
                    SatuanKonversiModel.konversi_id == konversi_id,
                    SatuanKonversiModel.deleted_at.is_(None),
                    SatuanKonversiModel.deleted_by.is_(None),
                )
            )
            .first()
        )

        if result:
            return await json_satuan_konversi(
                db=db,
                satuan_konversi_data_row=result,
                timestamp_data=timestamp_data,
                konversi_satuan_data=True,
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


async def create_data_satuan_konversi(db: Session, produk_id: int, satuan_konversi_data_create: SatuanKonversiReqSchema, identity: UsersBaseSchema):
    new_satuan_konversi = SatuanKonversiModel()
    try:
        new_satuan_konversi.konversi_produk = produk_id
        new_satuan_konversi.konversi_sku = satuan_konversi_data_create.konversi_sku
        new_satuan_konversi.konversi_satuan = satuan_konversi_data_create.konversi_satuan
        new_satuan_konversi.konversi_nilai = satuan_konversi_data_create.konversi_nilai
        new_satuan_konversi.konversi_harga = satuan_konversi_data_create.konversi_harga
        new_satuan_konversi.konversi_keterangan = satuan_konversi_data_create.konversi_keterangan
        new_satuan_konversi.konversi_aktif = satuan_konversi_data_create.konversi_aktif
        new_satuan_konversi.konversi_default = satuan_konversi_data_create.konversi_default

        new_satuan_konversi.created_at = datetime.now()
        new_satuan_konversi.created_by = identity.user_name

        db.add(new_satuan_konversi)
        db.commit()
        db.refresh(new_satuan_konversi)

        return await json_satuan_konversi(
            db=db,
            satuan_konversi_data_row=new_satuan_konversi
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

async def update_data_satuan_konversi(db: Session, produk_id: int, konversi_id: int, satuan_konversi_data_update: SatuanKonversiReqSchema, identity: UsersBaseSchema):
    try:
        old_satuan_konversi = await check_satuan_konversi(db, produk_id=produk_id, konversi_id=konversi_id)
        if old_satuan_konversi:
            old_satuan_konversi.konversi_sku = satuan_konversi_data_update.konversi_sku
            old_satuan_konversi.konversi_satuan = satuan_konversi_data_update.konversi_satuan
            old_satuan_konversi.konversi_nilai = satuan_konversi_data_update.konversi_nilai
            old_satuan_konversi.konversi_harga = satuan_konversi_data_update.konversi_harga
            old_satuan_konversi.konversi_keterangan = satuan_konversi_data_update.konversi_keterangan
            old_satuan_konversi.konversi_aktif = satuan_konversi_data_update.konversi_aktif
            old_satuan_konversi.konversi_default = satuan_konversi_data_update.konversi_default

            # Update data flag
            old_satuan_konversi.revised = (old_satuan_konversi.revised or 0) + 1
            old_satuan_konversi.updated_by = identity.user_name
            old_satuan_konversi.updated_at = datetime.now()

            db.commit()
            db.refresh(old_satuan_konversi)


            return await json_satuan_konversi(
                db=db,
                satuan_konversi_data_row=old_satuan_konversi
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
async def partial_update_data_satuan_konversi(db: Session, produk_id: int, konversi_id: int, satuan_konversi_data_update: dict, identity: UsersBaseSchema):
    try:
        old_patch_satuan_konversi = await check_satuan_konversi(db, produk_id=produk_id, konversi_id=konversi_id)
        if old_patch_satuan_konversi:
            # Update fields only if they are present in the provided data
            for field, value in satuan_konversi_data_update.items():
                if hasattr(old_patch_satuan_konversi, field):
                    setattr(old_patch_satuan_konversi, field, value)

            # Update data flag
            old_patch_satuan_konversi.revised = (old_patch_satuan_konversi.revised or 0) + 1
            old_patch_satuan_konversi.updated_by = identity.user_name
            old_patch_satuan_konversi.updated_at = datetime.now()

            db.commit()
            db.refresh(old_patch_satuan_konversi)

            return await json_satuan_konversi(
                db=db,
                satuan_konversi_data_row=old_patch_satuan_konversi
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
    
async def delete_data_satuan_konversi(db: Session, produk_id: int, konversi_id: int, identity: UsersBaseSchema):
    deleted_satuan_konversi = await check_satuan_konversi(db, produk_id=produk_id, konversi_id=konversi_id)
    try:
        deleted_satuan_konversi.konversi_aktif = 'Tidak Aktif'
        deleted_satuan_konversi.deleted_by = identity.user_name
        deleted_satuan_konversi.deleted_at = datetime.now()

        db.commit()
        db.refresh(deleted_satuan_konversi)

        return await json_satuan_konversi(
            db=db,
            satuan_konversi_data_row=deleted_satuan_konversi
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