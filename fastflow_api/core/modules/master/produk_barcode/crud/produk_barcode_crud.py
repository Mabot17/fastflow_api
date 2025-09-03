# ============================================= Start Noted CRUD ===================================
# Author : Abdul Rohman Masrifan | masrifan26@gamil.com
# 1. Response return wajib JSON/dict supaya bisa diolah kembali di router
# ============================================= END Noted CRUD ===================================
from sqlalchemy.orm import Session, aliased
from sqlalchemy import and_, func, or_
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from core.modules.master.produk_barcode.model.produk_barcode_model import ProdukBarcodeModel
from core.utils.common import SUCCESS, total_pages, start_from
from core.modules.master.produk_barcode.schema.produk_barcode_schema import ProdukBarcodeBaseDataSchema, ProdukBarcodeReqSchema, ProdukBarcodePutSchema, ProdukBarcodeRequestListSchema
from core.modules.users.schema.users_schema import UsersBaseSchema
from datetime import datetime
from typing import List, Optional, Dict

from core.shared.check_data_model import (
    check_produk_barcode,
)

from core.shared.json_helpers.master.json_produk_barcode import json_produk_barcode

import logging

async def get_crud_daftar_produk_barcode(db: Session, request: ProdukBarcodeRequestListSchema) -> List:
    try:
        produk_barcodeModel = aliased(ProdukBarcodeModel, name="produk_barcodeModel")

        query = db.query(produk_barcodeModel)
        if request.keywords and request.keywords.strip():
            keywords_lower = request.keywords.lower()
            query = query.filter(
                or_(
                    func.lower(produk_barcodeModel.productBarcode).like(f"%{keywords_lower}%"),
                    func.lower(produk_barcodeModel.productName).like(f"%{keywords_lower}%"),
                    func.lower(produk_barcodeModel.categoryNameLvl0).like(f"%{keywords_lower}%"),
                    func.lower(produk_barcodeModel.categoryNameLvl1).like(f"%{keywords_lower}%"),
                    func.lower(produk_barcodeModel.keterangan).like(f"%{keywords_lower}%")
                )
            )

        filter = []

        # Filter belum pernah dihapus
        filter.append(produk_barcodeModel.deleted_at.is_(None))
        filter.append(produk_barcodeModel.deleted_by.is_(None))
        
        # Filter berdasarkan aktif
        if request.aktif is not None and request.aktif != 'Semua' :
            filter.append(produk_barcodeModel.aktif == request.aktif)

        if request.categoryId is not None:
            filter.append(produk_barcodeModel.categoryIdLvl0 == request.categoryId)

        # Gabungkan semua filter menggunakan operator AND
        query = query.filter(and_(*filter))

        qr_count = query.count()
        count = qr_count

        qr_data = (
            query.order_by(produk_barcodeModel.productId.desc())
            .limit(request.results_per_page)
            .offset(start_from(request.page, request.results_per_page))
            .all()
        )

        result_data = [
            await json_produk_barcode(db=db, produk_barcode_data_row=row, timestamp_data=request.timestamp_data)
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

async def select_produk_barcode_by_id(
    db: Session,
    productId: int,
    timestamp_data: bool = False
) -> Dict:
    try:
        result = (
            db.query(ProdukBarcodeModel)
            .filter(
                and_(
                    ProdukBarcodeModel.productId == productId,
                    ProdukBarcodeModel.deleted_at.is_(None),
                    ProdukBarcodeModel.deleted_by.is_(None),
                )
            )
            .first()
        )

        if result:
            return await json_produk_barcode(
                db=db,
                produk_barcode_data_row=result,
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
    
async def select_produk_barcode_by_barcode(
    db: Session,
    productBarcode: str,
    timestamp_data: bool = False
) -> Dict:
    try:
        result = (
            db.query(ProdukBarcodeModel)
            .filter(
                and_(
                    ProdukBarcodeModel.productBarcode == productBarcode,
                    ProdukBarcodeModel.deleted_at.is_(None),
                    ProdukBarcodeModel.deleted_by.is_(None),
                )
            )
            .first()
        )

        if result:
            return await json_produk_barcode(
                db=db,
                produk_barcode_data_row=result,
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


async def create_data_produk_barcode(db: Session, produk_barcode_data_create: ProdukBarcodeReqSchema, identity: UsersBaseSchema):
    new_produk_barcode = ProdukBarcodeModel()
    try:
        new_produk_barcode.productBarcode = produk_barcode_data_create.productBarcode
        new_produk_barcode.productName = produk_barcode_data_create.productName
        new_produk_barcode.image = produk_barcode_data_create.image
        new_produk_barcode.sku = produk_barcode_data_create.sku
        new_produk_barcode.plu = produk_barcode_data_create.plu
        new_produk_barcode.categoryNameLvl0 = produk_barcode_data_create.categoryNameLvl0
        new_produk_barcode.categoryNameLvl1 = produk_barcode_data_create.categoryNameLvl1
        new_produk_barcode.categoryNameLvl2 = produk_barcode_data_create.categoryNameLvl2
        new_produk_barcode.categoryIdLvl0 = produk_barcode_data_create.categoryIdLvl0
        new_produk_barcode.categoryIdLvl1 = produk_barcode_data_create.categoryIdLvl1
        new_produk_barcode.categoryIdLvl2 = produk_barcode_data_create.categoryIdLvl2
        new_produk_barcode.stock = produk_barcode_data_create.stock
        new_produk_barcode.basePrice = produk_barcode_data_create.basePrice
        new_produk_barcode.finalPrice = produk_barcode_data_create.finalPrice
        new_produk_barcode.discountPercent = produk_barcode_data_create.discountPercent
        new_produk_barcode.discountQty = produk_barcode_data_create.discountQty
        new_produk_barcode.discountPrice = produk_barcode_data_create.discountPrice
        new_produk_barcode.discountValue = produk_barcode_data_create.discountValue

        new_produk_barcode.created_at = datetime.now()
        new_produk_barcode.created_by = identity.user_name

        db.add(new_produk_barcode)
        db.commit()
        db.refresh(new_produk_barcode)

        return await json_produk_barcode(
            db=db,
            produk_barcode_data_row=new_produk_barcode
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

async def update_data_produk_barcode(db: Session, productId: int, produk_barcode_data_update: ProdukBarcodePutSchema, identity: UsersBaseSchema):
    try:
        old_produk_barcode = await check_produk_barcode(db, productId=productId)
        if old_produk_barcode:
            old_produk_barcode.productId = produk_barcode_data_update.productId
            old_produk_barcode.productBarcode = produk_barcode_data_update.productBarcode
            old_produk_barcode.productName = produk_barcode_data_update.productName
            old_produk_barcode.image = produk_barcode_data_update.image
            old_produk_barcode.sku = produk_barcode_data_update.sku
            old_produk_barcode.plu = produk_barcode_data_update.plu
            old_produk_barcode.categoryNameLvl0 = produk_barcode_data_update.categoryNameLvl0
            old_produk_barcode.categoryNameLvl1 = produk_barcode_data_update.categoryNameLvl1
            old_produk_barcode.categoryNameLvl2 = produk_barcode_data_update.categoryNameLvl2
            old_produk_barcode.categoryIdLvl0 = produk_barcode_data_update.categoryIdLvl0
            old_produk_barcode.categoryIdLvl1 = produk_barcode_data_update.categoryIdLvl1
            old_produk_barcode.categoryIdLvl2 = produk_barcode_data_update.categoryIdLvl2
            old_produk_barcode.stock = produk_barcode_data_update.stock
            old_produk_barcode.basePrice = produk_barcode_data_update.basePrice
            old_produk_barcode.finalPrice = produk_barcode_data_update.finalPrice
            old_produk_barcode.discountPercent = produk_barcode_data_update.discountPercent
            old_produk_barcode.discountQty = produk_barcode_data_update.discountQty
            old_produk_barcode.discountPrice = produk_barcode_data_update.discountPrice
            old_produk_barcode.discountValue = produk_barcode_data_update.discountValue

            # Update data flag
            old_produk_barcode.revised = (old_produk_barcode.revised or 0) + 1
            old_produk_barcode.updated_by = identity.user_name
            old_produk_barcode.updated_at = datetime.now()

            db.commit()
            db.refresh(old_produk_barcode)


            return await json_produk_barcode(
                db=db,
                produk_barcode_data_row=old_produk_barcode
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
async def partial_update_data_produk_barcode(db: Session, productId: int, produk_barcode_data_update: dict, identity: UsersBaseSchema):
    try:
        old_patch_produk_barcode = await check_produk_barcode(db, productId=productId)
        if old_patch_produk_barcode:
            # Update fields only if they are present in the provided data
            for field, value in produk_barcode_data_update.items():
                if hasattr(old_patch_produk_barcode, field):
                    setattr(old_patch_produk_barcode, field, value)

            # Update data flag
            old_patch_produk_barcode.revised = (old_patch_produk_barcode.revised or 0) + 1
            old_patch_produk_barcode.updated_by = identity.user_name
            old_patch_produk_barcode.updated_at = datetime.now()

            db.commit()
            db.refresh(old_patch_produk_barcode)

            return await json_produk_barcode(
                db=db,
                produk_barcode_data_row=old_patch_produk_barcode
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
    
async def delete_data_produk_barcode(db: Session, productId: int, identity: UsersBaseSchema):
    deleted_produk_barcode = await check_produk_barcode(db, productId=productId)
    try:
        deleted_produk_barcode.aktif = 'Tidak Aktif'
        deleted_produk_barcode.deleted_by = identity.user_name
        deleted_produk_barcode.deleted_at = datetime.now()

        db.commit()
        db.refresh(deleted_produk_barcode)

        return await json_produk_barcode(
            db=db,
            produk_barcode_data_row=deleted_produk_barcode
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