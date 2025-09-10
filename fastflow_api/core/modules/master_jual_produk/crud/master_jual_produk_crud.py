# ============================================= Start Noted CRUD ===================================
# Author : PT. Dapur Perangkat Lunak Indonesia | KoffieSoft Group | https://www.koffiesoft.com/ | info@koffiesoft.com
# 1. Response return wajib JSON/dict supaya bisa diolah kembali di router
# ============================================= END Noted CRUD ===================================
from sqlalchemy.orm import Session, aliased
from sqlalchemy import and_, func, or_, select, text
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from core.modules.master_jual_produk.model.master_jual_produk_model import MasterJualProdukModel
from core.modules.master_jual_produk.model.detail_jual_produk_model import DetailJualProdukModel
from core.utils.common import SUCCESS, total_pages, start_from
from core.modules.master_jual_produk.schema.master_jual_produk_schema import (
    MasterJualProdukBaseDataSchema,
    MasterJualProdukReqSchema,
    MasterJualProdukPutSchema,
    MasterJualProdukRequestListSchema
)
from core.modules.users.schema.users_schema import UsersBaseSchema
from datetime import datetime
from typing import List, Optional, Dict

from core.shared.check_data_model import (
    check_master_jual_produk,
)

from core.shared.json_helpers.json_master_jual_produk import json_master_jual_produk

import logging

async def get_crud_daftar_master_jual_produk(db: Session, request: MasterJualProdukRequestListSchema) -> List:
    try:
        master_jual_produkModel = aliased(MasterJualProdukModel, name="master_jual_produkModel")

        query = db.query(master_jual_produkModel)
        if request.keywords and request.keywords.strip():
            keywords_lower = request.keywords.lower()
            query = query.filter(
                or_(
                    func.lower(master_jual_produkModel.jproduk_nobukti).like(f"%{keywords_lower}%"),
                    func.lower(master_jual_produkModel.jproduk_keterangan).like(f"%{keywords_lower}%")
                )
            )

        filter = []

        filter.append(
            or_(
                master_jual_produkModel.deleted_at.is_(None),
            )
        )
        filter.append(
            or_(
                master_jual_produkModel.deleted_by.is_(None),
            )
        )

        # Filter berdasarkan jproduk_stat_dok
        if request.jproduk_stat_dok is not None and request.jproduk_stat_dok != 'Semua' :
            filter.append(master_jual_produkModel.jproduk_stat_dok == request.jproduk_stat_dok)

        if request.jproduk_cust is not None and request.jproduk_cust != 0:
            filter.append(master_jual_produkModel.jproduk_cust == request.jproduk_cust)
        
        # Gabungkan semua filter menggunakan operator AND
        query = query.filter(and_(*filter))

        qr_count = query.count()
        count = qr_count

        qr_data = (
            query.order_by(master_jual_produkModel.jproduk_id.desc())
            .limit(request.results_per_page)
            .offset(start_from(request.page, request.results_per_page))
            .all()
        )

        result_data = [
            await json_master_jual_produk(db=db, master_jual_produk_data_row=row, timestamp_data=request.timestamp_data)
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

async def select_master_jual_produk_by_id(
    db: Session,
    jproduk_id: int,
    timestamp_data: bool = False
) -> Dict:
    try:
        result = (
            db.query(MasterJualProdukModel)
            .filter(
                and_(
                    MasterJualProdukModel.jproduk_id == jproduk_id,
                    MasterJualProdukModel.deleted_at.is_(None),
                    MasterJualProdukModel.deleted_by.is_(None),
                )
            )
            .first()
        )

        if result:
            return await json_master_jual_produk(
                db=db,
                master_jual_produk_data_row=result,
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

async def create_data_master_jual_produk(
    db: Session, 
    master_jual_produk_data_create: MasterJualProdukReqSchema, 
    identity: UsersBaseSchema
):
    from core.utils.generate_no_faktur import generate_master_jual_produk_nobukti
    new_master_jual_produk = MasterJualProdukModel()
    try:
        # generate nomor bukti otomatis
        new_master_jual_produk.jproduk_nobukti = await generate_master_jual_produk_nobukti(
            db=db, 
            tanggal=master_jual_produk_data_create.jproduk_tanggal, 
            identity=identity
        )
        new_master_jual_produk.jproduk_tanggal    = master_jual_produk_data_create.jproduk_tanggal
        new_master_jual_produk.jproduk_cust       = master_jual_produk_data_create.jproduk_cust
        new_master_jual_produk.jproduk_diskon     = master_jual_produk_data_create.jproduk_diskon
        new_master_jual_produk.jproduk_cara       = master_jual_produk_data_create.jproduk_cara
        new_master_jual_produk.jproduk_keterangan = master_jual_produk_data_create.jproduk_keterangan
        new_master_jual_produk.jproduk_stat_dok   = master_jual_produk_data_create.jproduk_stat_dok
        new_master_jual_produk.jproduk_bayar      = master_jual_produk_data_create.jproduk_bayar
        new_master_jual_produk.jproduk_totalbiaya = master_jual_produk_data_create.jproduk_totalbiaya

        # audit trail
        new_master_jual_produk.created_at = datetime.now()
        new_master_jual_produk.created_by = identity.user_name
        new_master_jual_produk.updated_at = datetime.now()
        new_master_jual_produk.updated_by = identity.user_name

        db.add(new_master_jual_produk)
        db.commit()
        db.refresh(new_master_jual_produk)

        return await json_master_jual_produk(
            db=db,
            master_jual_produk_data_row=new_master_jual_produk
        )
    except IntegrityError as e:
        logging.error(f"IntegrityError: {e}")
        return None
    except SQLAlchemyError as e:
        logging.error(f"SQLAlchemyError: {e}")
        return None
    except Exception as e:
        logging.error(e)
        return e


async def update_data_master_jual_produk(
    db: Session, 
    jproduk_id: int, 
    master_jual_produk_data_update: MasterJualProdukPutSchema, 
    identity: UsersBaseSchema
):
    try:
        old_master_jual_produk = await check_master_jual_produk(db, jproduk_id=jproduk_id)
        if old_master_jual_produk:
            old_master_jual_produk.jproduk_tanggal    = master_jual_produk_data_update.jproduk_tanggal
            old_master_jual_produk.jproduk_cust       = master_jual_produk_data_update.jproduk_cust
            old_master_jual_produk.jproduk_diskon     = master_jual_produk_data_update.jproduk_diskon
            old_master_jual_produk.jproduk_cara       = master_jual_produk_data_update.jproduk_cara
            old_master_jual_produk.jproduk_keterangan = master_jual_produk_data_update.jproduk_keterangan
            old_master_jual_produk.jproduk_stat_dok   = master_jual_produk_data_update.jproduk_stat_dok
            old_master_jual_produk.jproduk_bayar      = master_jual_produk_data_update.jproduk_bayar
            old_master_jual_produk.jproduk_totalbiaya = master_jual_produk_data_update.jproduk_totalbiaya

            # update audit trail
            old_master_jual_produk.revised    = (old_master_jual_produk.revised or 0) + 1
            old_master_jual_produk.updated_by = identity.user_name
            old_master_jual_produk.updated_at = datetime.now()

            db.commit()
            db.refresh(old_master_jual_produk)

            return await json_master_jual_produk(
                db=db,
                master_jual_produk_data_row=old_master_jual_produk
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
    
  
# Update method patch, jadi bisa diupdate salah satu kolom / bbrp kolom saja. tanpa pengecekan required dahulu
async def partial_update_data_master_jual_produk(db: Session, jproduk_id: int, master_jual_produk_data_update: dict, identity: UsersBaseSchema):
    try:
        old_patch_master_jual_produk = await check_master_jual_produk(db, jproduk_id=jproduk_id)
        if old_patch_master_jual_produk:
            # Update fields only if they are present in the provided data
            for field, value in master_jual_produk_data_update.items():
                if hasattr(old_patch_master_jual_produk, field):
                    setattr(old_patch_master_jual_produk, field, value)

            # Update data flag
            old_patch_master_jual_produk.revised = (old_patch_master_jual_produk.revised or 0) + 1
            old_patch_master_jual_produk.updated_by = identity.user_name
            old_patch_master_jual_produk.updated_at = datetime.now()

            db.commit()
            db.refresh(old_patch_master_jual_produk)

            return await json_master_jual_produk(
                db=db,
                master_jual_produk_data_row=old_patch_master_jual_produk
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
    
async def delete_data_master_jual_produk(db: Session, jproduk_id: int, identity: UsersBaseSchema):
    deleted_master_jual_produk = await check_master_jual_produk(db, jproduk_id=jproduk_id)
    try:
        deleted_master_jual_produk.jproduk_stat_dok = 'Batal'
        deleted_master_jual_produk.deleted_by = identity.user_name
        deleted_master_jual_produk.deleted_at = datetime.now()

        db.commit()
        db.refresh(deleted_master_jual_produk)

        return await json_master_jual_produk(
            db=db,
            master_jual_produk_data_row=deleted_master_jual_produk
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