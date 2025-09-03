from datetime import datetime
from pathlib import Path
import os
import pytz
from ..config import ZONA_WAKTU_SERVER, config
import re
from core.modules.users.schema.admin import UserAdminRole
from typing import List

# from user_agents import parse as uap
# from core.schemas.users.users import GrupUser
import logging
import decimal
from typing import Optional


STATUS_RECORD = {-1: "dihapus", 0: "non-aktif", 1: "aktif"}
ACCOUNT_STATUS = {0: "pending", 1: "verified"}
IMAGE_QUALITY_INITIAL = {"original": "", "medium": "M", "high": "H", "thumbnail": "T"}
HARI = {
    1: "Senin",
    2: "Selasa",
    3: "Rabu",
    4: "Kamis",
    5: "Jumat",
    6: "Sabtu",
    7: "Minggu",
}
BULAN = {
    1: "Januari",
    2: "Februari",
    3: "Maret",
    4: "April",
    5: "Mei",
    6: "Juni",
    7: "Juli",
    8: "Agustus",
    9: "September",
    10: "Oktober",
    11: "November",
    12: "Desember",
}
IS_PRIMARY = {0: "not_primary", 1: "primary"}
JENIS_KELAMIN = {1: "laki-laki", 2: "perempuan"}
STATUS_DIBACA = {0: "Belum", 1: "Sudah"}
SUCCESS = "success"
FAILED = "failed"

IMAGE_PLACEHOLDER_CAPTION = (
    "Ganti image default ini, dengan meng-upload atau menambahkan image yang berbeda."
)

NOTIF_TITLE = "Quick Count"


def start_from(page: int, resultperpage: int) -> int:
    return (page - 1) * resultperpage


def total_pages(total_records: int, records_per_page: int) -> int:
    div = total_records // records_per_page
    mod = total_records % records_per_page

    if mod > 0:
        return div + 1
    else:
        return div


def status_record_code(status_label):
    return list(STATUS_RECORD.keys())[list(STATUS_RECORD.values()).index(status_label)]


def create_folder_foto(foto_dir, subdir_name):
    if subdir_name:
        if not Path.exists(foto_dir / subdir_name):
            Path(foto_dir / subdir_name).mkdir(parents=True, exist_ok=True)
        return foto_dir / subdir_name
    else:
        if not Path.exists(foto_dir):
            Path(foto_dir).mkdir(parents=True, exist_ok=True)
        return foto_dir


def delete_file(foto_dir, subdir_name, filename):
    if subdir_name:
        del_foto = Path.joinpath(foto_dir, subdir_name, filename)
        if del_foto.is_file():
            os.remove(del_foto)
    else:
        del_foto = Path.joinpath(foto_dir, filename)
        if del_foto.is_file():
            os.remove(del_foto)


def ubah_zona_waktu(waktu: datetime, zw: str = ZONA_WAKTU_SERVER):
    if waktu:
        if zw == ZONA_WAKTU_SERVER:
            return waktu.astimezone(tz=pytz.timezone(zw))
        else:
            # Kalo timezonenya direplace, waktunya akan ada tambahan menit
            # return waktu.replace(tzinfo=pytz.timezone(ZONA_WAKTU_SERVER)).\
            #     astimezone(tz=pytz.timezone(zw))
            return waktu.astimezone(tz=pytz.timezone(zw))
    else:
        return None


def waktu_to_isoformat(waktu: datetime, timespec: str = "seconds"):
    if waktu:
        return waktu.isoformat(timespec=timespec)
    else:
        return None


def format_rupiah(nilai: decimal.Decimal):
    return f"{int(nilai):,}".replace(",", ".")


def tgl_indo(waktu: datetime):
    if waktu:
        bulan_str = BULAN[waktu.month]
        return f"{waktu.day} {bulan_str} {waktu.year}"
    else:
        return ""


def waktu_to_indonesia_format(waktu: datetime):
    if waktu:
        bulan_str = BULAN[waktu.month]
        return (
            f"{waktu.day} {bulan_str} {waktu.year} "
            f"pukul {waktu.hour:02d}:{waktu.minute:02d} WIB"
        )
    else:
        return ""


def zona_waktu_indonesia(zw: str = ZONA_WAKTU_SERVER):
    if zw == "Asia/Jakarta" or zw == "Asia/Pontianak":
        return "WIB"
    elif zw == "Asia/Makassar":
        return "WITA"
    elif zw == "Asia/Jayapura":
        return "WIT"
    else:
        return "Zona waktu untuk Indonesia tidak dikenali"


def convert_durasi_range(min, max: int) -> str:
    return f"{min}-{max}"


def convert_durasi_unit(unit_name: str) -> str:
    if unit_name.lower().strip() == "day":
        return "hari"
    elif unit_name.lower().strip() == "hour":
        return "jam"


def validasi_nomor_hp_indonesia(nomor: str) -> bool:
    # valid format : 08123456789
    # 08563030408
    nomor_regex = re.compile(r"^(0)8[1-9][0-9]{6,10}$")
    matching = nomor_regex.search(nomor)
    if matching:
        return True
    else:
        return False


def normalize_phone_number(phone: str) -> str:
    # Hapus semua karakter selain angka
    digits = re.sub(r'\D', '', phone)
    
    if digits.startswith("0"):
        digits = "62" + digits[1:]
    elif digits.startswith("62"):
        pass
    elif digits.startswith("8"):
        digits = "62" + digits

    return digits



def validasi_password(pswd: str):
    """Check if the password is valid.

    This function checks the following conditions
    if its length is greater than 6 and less than 8
    if it has at least one uppercase letter
    if it has at least one lowercase letter
    if it has at least one numeral
    if it has any of the required special symbols
    """
    SpecialSym = ["$", "@", "#"]
    return_val = True
    message = ""
    if len(pswd) < 8:
        message = "Panjang password tidak boleh kurang dari 8"
        return_val = False
    if len(pswd) > 20:
        message = "Panjang password tidak boleh lebih dari 20"
        return_val = False
    if not any(char.isdigit() for char in pswd):
        message = "Password harus memiliki minimal 1 angka"
        return_val = False
    if not any(char.isupper() for char in pswd):
        message = "Password harus memiliki minimal 1 huruf besar"
        return_val = False
    if not any(char.islower() for char in pswd):
        message = "Password harus memiliki minimal 1 huruf kecil"
        return_val = False
    if not any(char in SpecialSym for char in pswd):
        message = "Password harus memiliki minimal 1 simbol ($, @, atau #)"
        return_val = False
    return {"result": return_val, "message": message}


def is_valid_grup_access(
    allowed_grup: str,
    tested_grup: str,
    allowed_admin_role: UserAdminRole = None,
    tested_admin_role: str = None,
):
    if tested_grup != allowed_grup:
        return False, {
            "status": {
                "kode": FAILED,
                "keterangan": "User ini tidak memiliki hak akses grup",
            },
            "data": None,
        }
    else:
        if allowed_admin_role:
            if allowed_admin_role.value != tested_admin_role:
                return False, {
                    "status": {
                        "kode": FAILED,
                        "keterangan": "User ini tidak memiliki hak akses grup",
                    },
                    "data": None,
                }
            else:
                return True, None
        else:
            return True, None

def is_valid_access_by_id_user(
    allowed_id: int, tested_id: int
) -> tuple[bool, Optional[dict]]:
    if allowed_id != tested_id:
        return False, {
            "status": {
                "kode": FAILED,
                "keterangan": "User ini tidak memiliki hak akses",
            },
            "data": None,
        }
    else:
        return True, None


# def device_by_user_agent_or_param(user_agent: str = None,
#                                   device_from_param: str = None):
#     # Default device adalah None artinya dianggap valid dari device apapun
#     device = None

#     # Jika ada user_agent, maka tipe device akan diekstrak dari user_agent
#     if user_agent:
#         u_agent = uap(user_agent)
#         logging.debug(f'device: {u_agent.get_device()}')
#         logging.debug(f'os: {u_agent.get_os()}')
#         logging.debug(f'browser: {u_agent.get_browser()}')
#         if u_agent.get_device() == 'PC':
#             device = DeviceVoucher.WEB.value
#         else:
#             dv_values = [item.value for item in DeviceVoucher]
#             if u_agent.get_os().lower() in dv_values:
#                 device = u_agent.get_os().lower()

#     # Jika ada device dari param, maka tipe device diambil dari param device
#     if device_from_param:
#         dv_values = [item.value for item in DeviceVoucher]
#         if device_from_param.lower() in dv_values:
#             device = device_from_param

#     return device


def log_config_is_active(config_name: str) -> bool:
    if config_name in config:
        logging.debug("log_config_is_active: exists in config")
        if config[config_name] == "1" or config[config_name] == 1:
            return True
        else:
            return False
    else:
        # Jika tidak ditemukan setting spesifik di file .env maka
        # dianggap loggernya aktif untuk menjaga kemungkinan typo
        logging.debug("log_config_is_active: NOT exists in config")
        return True

def extract_esb_member_core_to_loop_code(input_str):
    parts = input_str.split('#')
    return parts[1].strip() if len(parts) > 1 else None

