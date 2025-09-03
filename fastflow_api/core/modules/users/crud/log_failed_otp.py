from datetime import datetime, date
import logging
from core.config import ZONA_WAKTU_SERVER
from ...models.users.log_failed_otp import LogFailedOTPModel
from sqlalchemy.orm import Session, aliased
from sqlalchemy import func, and_
from ...utils.common import (
    STATUS_DIBACA,
    SUCCESS,
    start_from,
    total_pages,
    ubah_zona_waktu,
    waktu_to_isoformat,
    zona_waktu_indonesia,
)
from typing import List
from typing import Optional
from ...models.users.users_model import UsersModel
import pyotp


async def json_log_failed_otp(
    db: Session, log: LogFailedOTPModel, zona_waktu: str = ZONA_WAKTU_SERVER
):
    return_data = {
        "id": log.id,
        "user_id": log.user_id,
        "failed_otp": log.tested_otp,
        "otp_seharusnya": log.valid_otp,
        "notes": log.notes,
        "created_at": {
            "waktu": waktu_to_isoformat(ubah_zona_waktu(log.created_at, zw=zona_waktu)),
            "waktu_indonesia": zona_waktu_indonesia(zona_waktu),
        },
    }

    return return_data


async def add_failed_otp_to_log(
    db: Session,
    user: UsersModel,
    tested_otp: str,
    otp_obj: pyotp.TOTP,
    on_module: Optional[str] = "",
) -> LogFailedOTPModel:
    log = LogFailedOTPModel()
    try:
        log.user_id = user.id
        log.tested_otp = tested_otp
        log.valid_otp = otp_obj.now()
        log.notes = f"HP: {user.hp} - Email: {user.email} - {user.secret_key} - mod: {on_module}"
        log.created_at = datetime.now()
        log.created_by = "system"

        db.add(log)
        db.commit()
        db.refresh(log)

        return log
    except Exception as e:
        logging.error(e)
        return None


async def del_failed_otp_from_log(db: Session, log: LogFailedOTPModel):
    try:
        db.delete(log)
        db.commit()

        return True
    except Exception as e:
        logging.error(e)
        return False


async def select_all_log_failed_otp(
    db: Session,
    tgl_awal: Optional[date],
    tgl_akhir: Optional[date],
    hp: Optional[str],
    email: Optional[str],
    page: int = 1,
    results_per_page: int = 20,
    zona_waktu: str = ZONA_WAKTU_SERVER,
) -> List:
    fo = aliased(LogFailedOTPModel, name="fo")
    u = aliased(UsersModel, name="u")

    filter = []
    filter.append(u.deleted_at.is_(None))
    filter.append(u.deleted_by.is_(None))
    filter.append(fo.deleted_at.is_(None))
    filter.append(fo.deleted_by.is_(None))
    if tgl_awal:
        filter.append(func.date(fo.created_at) >= tgl_awal)
    if tgl_akhir:
        filter.append(func.date(fo.created_at) <= tgl_akhir)
    if hp:
        filter.append(u.hp.contains(hp.strip()))
    if email:
        filter.append(u.email.contains(email.strip()))
    criterion = and_(*filter)

    qr_count = (
        db.query(func.count(fo.id))
        .join(u, u.id == fo.user_id, isouter=True)
        .filter(criterion)
        .one()
    )
    count = [row for row in qr_count][0]
    pages = total_pages(count, results_per_page)

    qr_data = (
        db.query(fo)
        .join(u, u.id == fo.user_id, isouter=True)
        .filter(criterion)
        .order_by(fo.created_at.desc())
        .limit(results_per_page)
        .offset(start_from(page, results_per_page))
        .all()
    )
    datas = [
        await json_log_failed_otp(db, log=row, zona_waktu=zona_waktu) for row in qr_data
    ]

    return {
        "status": {"kode": SUCCESS, "keterangan": SUCCESS},
        "paging": {
            "page": page,
            "total_pages": pages,
            "records_per_page": results_per_page,
        },
        "data": datas,
    }
