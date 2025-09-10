# ============================================= Start Noted CRUD ===================================
# Author : PT. Dapur Perangkat Lunak Indonesia | KoffieSoft Group | https://www.koffiesoft.com/ | info@koffiesoft.com
# 1. Response return wajib JSON/dict supaya bisa diolah kembali di router
# ============================================= END Noted CRUD ===================================
from sqlalchemy.orm import Session, aliased
from sqlalchemy import and_, func, or_
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from core.modules.master_jual_produk.model.detail_jual_produk_model import DetailJualProdukModel
from core.utils.common import SUCCESS, total_pages, start_from
from core.modules.master_jual_produk.schema.detail_jual_produk_schema import (
    DetailMasterJualProdukBaseDataSchema,
    DetailMasterJualProdukReqSchema,
    DetailMasterJualProdukRequestListSchema
)
from core.modules.users.schema.users_schema import UsersBaseSchema
from datetime import datetime
from typing import List, Optional, Dict

from core.shared.check_data_model import (
    check_detail_jual_produk,
)

from core.shared.json_helpers.json_detail_jual_produk import json_detail_jual_produk

import logging

async def get_crud_daftar_detail_jual_produk(db: Session, jproduk_id : int, request: DetailMasterJualProdukRequestListSchema) -> List:
    try:
        detail_jual_produk_model = aliased(DetailJualProdukModel, name="detail_jual_produk_model")

        query = db.query(detail_jual_produk_model)
        filter = []

        # Filter berdasarkan deleted_at
        filter.append(detail_jual_produk_model.deleted_by.is_(None))
        filter.append(
            or_(
                detail_jual_produk_model.deleted_at.is_(None),
                detail_jual_produk_model.deleted_at == "0000-00-00 00:00:00"
            )
        )

        if jproduk_id:
            filter.append(detail_jual_produk_model.dproduk_master == jproduk_id)
        
        # Gabungkan semua filter menggunakan operator AND
        query = query.filter(and_(*filter))

        qr_count = query.count()
        count = qr_count

        qr_data = (
            query.order_by(detail_jual_produk_model.dproduk_id)
            .limit(request.results_per_page)
            .offset(start_from(request.page, request.results_per_page))
            .all()
        )

        result_data = [
            await json_detail_jual_produk(db=db, detail_jual_produk_data_row=row, timestamp_data=request.timestamp_data, dproduk_produk_data=request.dproduk_produk_data, dproduk_satuan_data=request.dproduk_satuan_data)
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

async def select_detail_jual_produk_by_id(
    db: Session,
    jproduk_id: int,
    dproduk_id: int,
    timestamp_data: bool = False
) -> Dict:
    try:
        result = (
            db.query(DetailJualProdukModel)
            .filter(
                and_(
                    DetailJualProdukModel.dproduk_master == jproduk_id,
                    DetailJualProdukModel.dproduk_id == dproduk_id,
                    DetailJualProdukModel.deleted_by.is_(None),
                    or_(
                        DetailJualProdukModel.deleted_at.is_(None),
                        DetailJualProdukModel.deleted_at == "0000-00-00 00:00:00"
                    )
                )
            )
            .first()
        )

        if result:
            return await json_detail_jual_produk(
                db=db,
                detail_jual_produk_data_row=result,
                dproduk_produk_data=True,
                dproduk_satuan_data=True,
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


async def create_data_detail_jual_produk(db: Session, jproduk_id: int, detail_jual_produk_data_create: DetailMasterJualProdukReqSchema, identity: UsersBaseSchema):
    new_detail_jual_produk = DetailJualProdukModel()
    try:
        new_detail_jual_produk.dproduk_master = jproduk_id
        new_detail_jual_produk.dproduk_produk = detail_jual_produk_data_create.dproduk_produk
        new_detail_jual_produk.dproduk_satuan = detail_jual_produk_data_create.dproduk_satuan
        new_detail_jual_produk.dproduk_jumlah = detail_jual_produk_data_create.dproduk_jumlah
        new_detail_jual_produk.dproduk_harga = detail_jual_produk_data_create.dproduk_harga
        new_detail_jual_produk.dproduk_diskon = detail_jual_produk_data_create.dproduk_diskon
        new_detail_jual_produk.dproduk_diskon_rp = detail_jual_produk_data_create.dproduk_diskon_rp

        new_detail_jual_produk.created_at = datetime.now()
        new_detail_jual_produk.created_by = identity.user_name
        new_detail_jual_produk.updated_at = datetime.now()
        new_detail_jual_produk.updated_by = identity.user_name

        db.add(new_detail_jual_produk)
        db.commit()
        db.refresh(new_detail_jual_produk)

        return await json_detail_jual_produk(
            db=db,
            dproduk_produk_data=True,
            dproduk_satuan_data=True,
            detail_jual_produk_data_row=new_detail_jual_produk
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

async def update_data_detail_jual_produk(db: Session, jproduk_id: int, dproduk_id: int, detail_jual_produk_data_update: DetailMasterJualProdukReqSchema, identity: UsersBaseSchema):
    try:
        old_detail_jual_produk = await check_detail_jual_produk(db, dproduk_id=dproduk_id, jproduk_id=jproduk_id)
        if old_detail_jual_produk:
            old_detail_jual_produk.dproduk_produk = detail_jual_produk_data_update.dproduk_produk
            old_detail_jual_produk.dproduk_satuan = detail_jual_produk_data_update.dproduk_satuan
            old_detail_jual_produk.dproduk_jumlah = detail_jual_produk_data_update.dproduk_jumlah
            old_detail_jual_produk.dproduk_harga = detail_jual_produk_data_update.dproduk_harga
            old_detail_jual_produk.dproduk_diskon = detail_jual_produk_data_update.dproduk_diskon
            old_detail_jual_produk.dproduk_diskon_rp = detail_jual_produk_data_update.dproduk_diskon_rp

            # Update data flag
            old_detail_jual_produk.revised = (old_detail_jual_produk.revised or 0) + 1
            old_detail_jual_produk.updated_by = identity.user_name
            old_detail_jual_produk.updated_at = datetime.now()

            db.commit()
            db.refresh(old_detail_jual_produk)


            return await json_detail_jual_produk(
                db=db,
                dproduk_produk_data=True,
                dproduk_satuan_data=True,
                detail_jual_produk_data_row=old_detail_jual_produk
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
async def partial_update_data_detail_jual_produk(db: Session, jproduk_id: int, dproduk_id: int, detail_jual_produk_data_update: dict, identity: UsersBaseSchema):
    try:
        old_patch_detail_jual_produk = await check_detail_jual_produk(db, dproduk_id=dproduk_id, jproduk_id=jproduk_id)
        if old_patch_detail_jual_produk:
            # Update fields only if they are present in the provided data
            for field, value in detail_jual_produk_data_update.items():
                if hasattr(old_patch_detail_jual_produk, field):
                    setattr(old_patch_detail_jual_produk, field, value)

            # Update data flag
            old_patch_detail_jual_produk.revised = (old_patch_detail_jual_produk.revised or 0) + 1
            old_patch_detail_jual_produk.updated_by = identity.user_name
            old_patch_detail_jual_produk.updated_at = datetime.now()

            db.commit()
            db.refresh(old_patch_detail_jual_produk)

            return await json_detail_jual_produk(
                db=db,
                dproduk_produk_data=True,
                dproduk_satuan_data=True,
                detail_jual_produk_data_row=old_patch_detail_jual_produk
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
    
async def delete_data_detail_jual_produk(db: Session, jproduk_id: int, dproduk_id: int, identity: UsersBaseSchema):
    deleted_detail_jual_produk = await check_detail_jual_produk(db, dproduk_id=dproduk_id, jproduk_id=jproduk_id)
    try:
        deleted_detail_jual_produk.dproduk_harga = 'Tidak Aktif'
        deleted_detail_jual_produk.deleted_by = identity.user_name
        deleted_detail_jual_produk.deleted_at = datetime.now()

        db.commit()
        db.refresh(deleted_detail_jual_produk)

        return await json_detail_jual_produk(
            db=db,
            dproduk_produk_data=True,
            dproduk_satuan_data=True,
            detail_jual_produk_data_row=deleted_detail_jual_produk
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