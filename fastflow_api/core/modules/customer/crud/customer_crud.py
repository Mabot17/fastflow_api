# ============================================= Start Noted CRUD ===================================
# Author : PT. Dapur Perangkat Lunak Indonesia | KoffieSoft Group | https://www.koffiesoft.com/ | info@koffiesoft.com
# 1. Response return wajib JSON/dict supaya bisa diolah kembali di router
# ============================================= END Noted CRUD ===================================
from sqlalchemy.orm import Session, aliased
from sqlalchemy import and_, func, or_
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from core.modules.customer.model.customer_model import CustomerModel
from core.utils.common import SUCCESS, total_pages, start_from
from core.modules.customer.schema.customer_schema import CustomerBaseDataSchema, CustomerReqSchema, CustomerPutSchema, CustomerRequestListSchema
from core.modules.users.schema.users_schema import UsersBaseSchema
from datetime import datetime
from typing import List, Optional, Dict

from core.shared.check_data_model import (
    check_customer,
)

from core.shared.json_helpers.json_customer import json_customer

import logging

async def get_crud_daftar_customer(db: Session, request: CustomerRequestListSchema) -> List:
    try:
        customerModel = aliased(CustomerModel, name="customerModel")

        query = db.query(customerModel)
        if request.keywords and request.keywords.strip():
            keywords_lower = request.keywords.lower()
            query = query.filter(
                or_(
                    func.lower(customerModel.cust_no).like(f"%{keywords_lower}%"),
                    func.lower(customerModel.cust_nama_lengkap).like(f"%{keywords_lower}%"),
                    func.lower(customerModel.cust_keterangan).like(f"%{keywords_lower}%")
                )
            )

        filter = []

        # Filter belum pernah dihapus
        filter.append(
            or_(
                customerModel.deleted_at.is_(None),
                customerModel.deleted_at == "0000-00-00 00:00:00"
            )
        )
        filter.append(customerModel.deleted_by.is_(None))
        

        # Filter berdasarkan cust_aktif
        if request.cust_aktif is not None:
            if request.cust_aktif == 'Aktif':
                filter.append(customerModel.cust_aktif == 'Aktif')
            elif request.cust_aktif == 'Tidak Aktif':
                filter.append(customerModel.cust_aktif == 'Tidak Aktif')
        
        # Gabungkan semua filter menggunakan operator AND
        query = query.filter(and_(*filter))

        qr_count = query.count()
        count = qr_count

        qr_data = (
            query.order_by(customerModel.cust_id.desc())
            .limit(request.results_per_page)
            .offset(start_from(request.page, request.results_per_page))
            .all()
        )

        result_data = [
            await json_customer(db=db, customer_data_row=row, timestamp_data=request.timestamp_data)
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

async def select_customer_by_id(
    db: Session,
    cust_id: int,
    timestamp_data: bool = False
) -> Dict:
    try:
        result = (
            db.query(CustomerModel)
            .filter(
                and_(
                    CustomerModel.cust_id == cust_id,
                    or_(
                        CustomerModel.deleted_at.is_(None),
                        CustomerModel.deleted_at == "0000-00-00 00:00:00"
                    ),
                    CustomerModel.deleted_by.is_(None),
                )
            )
            .first()
        )

        print(result)

        if result:
            return await json_customer(
                db=db,
                customer_data_row=result,
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

async def create_data_customer(db: Session, customer_data_create: CustomerReqSchema, identity: UsersBaseSchema):
    new_customer = CustomerModel()
    try:
        new_customer.cust_no             = customer_data_create.cust_no
        new_customer.cust_nama_lengkap   = customer_data_create.cust_nama_lengkap
        new_customer.cust_nama_panggilan = customer_data_create.cust_nama_panggilan
        new_customer.cust_kelamin        = customer_data_create.cust_kelamin
        new_customer.cust_alamat         = customer_data_create.cust_alamat
        new_customer.cust_hp             = customer_data_create.cust_hp
        new_customer.cust_aktif          = customer_data_create.cust_aktif
        new_customer.cust_keterangan     = customer_data_create.cust_keterangan

        new_customer.created_at = datetime.now()
        new_customer.created_by = identity.user_name

        db.add(new_customer)
        db.commit()
        db.refresh(new_customer)

        return await json_customer(
            db=db,
            customer_data_row=new_customer
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
        logging.error(f"Unexpected Error: {e}")
        db.rollback()
        return None


async def update_data_customer(db: Session, cust_id: int, customer_data_update: CustomerPutSchema, identity: UsersBaseSchema):
    try:
        old_customer = await check_customer(db, cust_id=cust_id)
        if old_customer:
            old_customer.cust_no             = customer_data_update.cust_no
            old_customer.cust_nama_lengkap   = customer_data_update.cust_nama_lengkap
            old_customer.cust_nama_panggilan = customer_data_update.cust_nama_panggilan
            old_customer.cust_kelamin        = customer_data_update.cust_kelamin
            old_customer.cust_alamat         = customer_data_update.cust_alamat
            old_customer.cust_hp             = customer_data_update.cust_hp
            old_customer.cust_aktif          = customer_data_update.cust_aktif
            old_customer.cust_keterangan     = customer_data_update.cust_keterangan

            # Update flag revisi dan metadata
            old_customer.revised    = (old_customer.revised or 0) + 1
            old_customer.updated_by = identity.user_name
            old_customer.updated_at = datetime.now()

            db.commit()
            db.refresh(old_customer)

            return await json_customer(
                db=db,
                customer_data_row=old_customer
            )
        else:
            return None
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
async def partial_update_data_customer(db: Session, cust_id: int, customer_data_update: dict, identity: UsersBaseSchema):
    try:
        old_patch_customer = await check_customer(db, cust_id=cust_id)
        if old_patch_customer:
            # Update fields only if they are present in the provided data
            for field, value in customer_data_update.items():
                if hasattr(old_patch_customer, field):
                    setattr(old_patch_customer, field, value)

            # Update data flag
            old_patch_customer.revised = (old_patch_customer.revised or 0) + 1
            old_patch_customer.updated_by = identity.user_name
            old_patch_customer.updated_at = datetime.now()

            db.commit()
            db.refresh(old_patch_customer)

            return await json_customer(
                db=db,
                customer_data_row=old_patch_customer
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
    
async def delete_data_customer(db: Session, cust_id: int, identity: UsersBaseSchema):
    deleted_customer = await check_customer(db, cust_id=cust_id)
    try:
        deleted_customer.cust_aktif = 'Tidak Aktif'
        deleted_customer.deleted_by = identity.user_name
        deleted_customer.deleted_at = datetime.now()

        db.commit()
        db.refresh(deleted_customer)

        return await json_customer(
            db=db,
            customer_data_row=deleted_customer
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