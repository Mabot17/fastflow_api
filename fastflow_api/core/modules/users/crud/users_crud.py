# ============================================= Start Noted CRUD ===================================
# Author : Abdul Rohman Masrifan | https://fastflow.pybot.cloud/ | masrifan26@gmail.com
# 1. Response return wajib JSON/dict supaya bisa diolah kembali di router
# ============================================= END Noted CRUD ===================================
import hashlib
from sqlalchemy.orm import Session, aliased
from sqlalchemy import func, and_, or_, text
from sqlalchemy.exc import IntegrityError
from core.modules.users.model.users_model import (
    UsersModel,
)

from typing import Optional, List, Dict
from core.modules.users.schema.users_schema import (
    UsersBaseSchema,
    UsersReqSchema,
    UsersRequestListSchema
)
import logging
from datetime import datetime
from core.utils.hashing import Hash

from core.shared.check_data_model import (
    check_users,
)


from core.utils.upload_foto import upload_image_file, upload_aws_image_file
from core.shared.json_helpers.json_user import json_user

import logging


async def get_crud_list_users(db: Session, request : UsersRequestListSchema = None) -> List:
    from core.utils.common import start_from
    try:
        usersModel = aliased(UsersModel, name="usersModel")

        query = db.query(usersModel)
        if request.keywords and request.keywords.strip():
            keyword = request.keywords.lower()
            query = query.filter(
                or_(
                    func.lower(usersModel.user_name).contains(keyword),
                    func.lower(usersModel.user_kode).contains(keyword)
                )
            )

        filter = []

        # Filter berdasarkan user_aktif
        if request.user_aktif is not None:
            if request.user_aktif == 'Aktif':
                filter.append(usersModel.user_aktif == 'Aktif')
                # Filter belum pernah dihapus
                filter.append(usersModel.deleted_at.is_(None))
                filter.append(usersModel.deleted_by.is_(None))
            elif request.user_aktif == 'Tidak Aktif':
                filter.append(usersModel.user_aktif == 'Tidak Aktif')
        else:
            filter.append(usersModel.user_aktif == 'Aktif')

        # Gabungkan semua filter menggunakan operator AND
        query = query.filter(and_(*filter))

        qr_count = query.count()
        count = qr_count

        qr_data = (
            query.order_by(usersModel.user_id)
            .limit(request.results_per_page)
            .offset(start_from(request.page, request.results_per_page))
            .all()
        )
        result_data = [
            await json_user(db=db, user_data_row=row, timestamp_data=request.timestamp_data)
            for row in qr_data
        ]

        if result_data:  # Check if result_data is not an empty list
            return {"data": result_data, "total_data" : count}
        else:
            return {"data": None, "total_data" : 0}
    except IntegrityError as e:
        logging.error(f"IntegrityError: {e}")
        return None  # Tangani kesalahan unik di endpoint
    except Exception as e:
        logging.error(f"Exception: {e}")

async def select_user_by_id(
    db: Session,
    user_id: int,
    timestamp_data: bool = False,
) -> Dict:
    
    try:
        result = (
            db.query(UsersModel)
            .filter(
                and_(
                    UsersModel.user_id == user_id,
                    UsersModel.deleted_at.is_(None),
                    UsersModel.deleted_by.is_(None),
                )
            )
            .first()
        )

        if result:
            return await json_user(
                db=db,
                user_data_row=result,
                timestamp_data=timestamp_data,
            )
        else:
            return None
    except IntegrityError as e:
        logging.error(f"IntegrityError: {e}")
        return None  # Tangani kesalahan unik di endpoint
    except Exception as e:
        logging.error(f"Exception: {e}")

async def create_data_user(db: Session, user_data_create: UsersReqSchema):
    new_user = UsersModel()
    try:
        new_user.user_name = user_data_create.user_name
        new_user.user_kode = user_data_create.user_kode
        new_user.user_aktif = user_data_create.user_aktif
        new_user.user_keterangan = user_data_create.user_keterangan
        new_user.created_by = user_data_create.user_name
        new_user.created_at = datetime.now()

        if user_data_create.password:
            value_pass_sha = Hash.pbkdf2_sha256(user_data_create.password)
            value_pass_md5 = hashlib.md5(user_data_create.password.encode('utf-8')).hexdigest()
            new_user.user_password = value_pass_sha

        db.add(new_user)
        db.commit()
        db.refresh(new_user)

        return await json_user(
            db=db,
            user_data_row=new_user
        )
    
    except Exception as e:
        logging.error(e)
        return None

async def update_data_user(db: Session, user_data_update: UsersReqSchema, user_id: int, identity=UsersBaseSchema):
    old_user = await check_users(db, user_id=user_id)
    if old_user:
        try:
            old_user.user_name = user_data_update.user_name
            old_user.user_kode = user_data_update.user_kode
            old_user.user_aktif = user_data_update.user_aktif
            old_user.user_keterangan = user_data_update.user_keterangan
            old_user.revised = (old_user.revised or 0) + 1
            old_user.updated_by = identity.user_name
            old_user.updated_at = datetime.now()

            db.commit()
            db.refresh(old_user)

            return await json_user(
                db=db,
                user_data_row=old_user
            )
        except Exception as e:
            logging.error(e)
            return str(e)
    else:
        return None

# Update method patch, jadi bisa diupdate salah satu kolom / bbrp kolom saja. tanpa pengecekan required dahulu
async def partial_update_data_user(db: Session, user_id: int, user_data_update: dict, identity: UsersBaseSchema):
    try:
        old_patch_user = await check_users(db, user_id=user_id)
        if old_patch_user:
            # Update fields only if they are present in the provided data (khusus yang ada saja di array JSON)
            for field, value in user_data_update.items():
                if field == "password":
                    value_pass_sha = Hash.pbkdf2_sha256(value)
                    value_pass_md5 = hashlib.md5(value.encode('utf-8')).hexdigest()

                    setattr(old_patch_user, 'user_password', value_pass_sha)
                    # Menghitung hash MD5
                elif hasattr(old_patch_user, field):
                    setattr(old_patch_user, field, value)

            # Update data flag
            old_patch_user.revised = (old_patch_user.revised or 0) + 1
            old_patch_user.updated_by = identity.user_name
            old_patch_user.updated_at = datetime.now()

            db.commit()
            db.refresh(old_patch_user)

            return await json_user(
                db=db,
                user_data_row=old_patch_user
            )
        else:
            return None
    except IntegrityError as e:
        logging.error(f"IntegrityError: {e}")
        return None  # Tangani kesalahan unik di endpoint
    except Exception as e:
        logging.error(f"Exception: {e}")

async def delete_data_user(db: Session, user_id, identity=UsersBaseSchema):
    user = await check_users(db, user_id=user_id)
    try:
        user.user_aktif = 'Tidak Aktif'
        user.deleted_by = identity.user_name
        user.deleted_at = datetime.now()

        db.commit()
        db.refresh(user)

        return await json_user(
            db=db,
            user_data_row=user
        )
    except Exception as e:
        logging.error(e)
        return None
    
def save_user_otp_code(db: Session, username: str, secret: str):
    user = db.query(UsersModel).filter(UsersModel.user_name == username).first()
    if user:
        user.user_otp_code = secret
        db.commit()
        db.refresh(user)
        return user
    else:
        return None