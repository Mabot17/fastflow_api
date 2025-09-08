# ============================================= Start Noted generate data ===================================
# Author : Abdul Rohman Masrifan | https://fastflow.pybot.cloud/ | masrifan26@gmail.com
# 1. Response return wajib JSON/dict supaya bisa diolah kembali di router
# ============================================= END Noted generate data ===================================
from datetime import date, datetime
import re
from sqlalchemy.orm import Session, aliased
from sqlalchemy import and_, func, or_
from sqlalchemy.exc import IntegrityError

# Import model
from core.modules.produk.model.produk_model import ProdukModel
from core.modules.produk_group.model.produk_group_model import ProdukGroupModel
from core.modules.users.schema.users_schema import UsersBaseSchema

# Import cek data model
from core.shared.check_data_model import (
    check_user_by_username,
    check_produk_group
)

async def generate_produk_kode(db: Session, produk_group: int) -> str:
    data_group_produk = await check_produk_group(db, group_id=produk_group)
    prefix = f"{data_group_produk.group_kode}"

    last_record = db.query(ProdukModel.produk_kode).filter(
        ProdukModel.produk_kode.like(f"{prefix}%")
    ).order_by(ProdukModel.produk_kode.desc()).first()

    last_running_number = 1
    if last_record and last_record.produk_kode:
        match = re.search(rf"{re.escape(prefix)}(\d+)$", last_record.produk_kode)
        if match:
            last_running_number = int(match.group(1)) + 1

    return f"{prefix}{last_running_number:03d}"

