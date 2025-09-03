# ============================================= Start Noted JSON Global ===================================
# Author : Abdul Rohman Masrifan | masrifan26@gamil.com
# 1. Response return wajib JSON/dict supaya bisa diolah kembali di router
# 2. Menampung dan membuat semua response disini, karena supaya bisa dipakai lagi oleh object yang lain
# 3. Definisikan JSON global seperti timestamp, approval dll
# ============================================= END Noted JSON Global ===================================
from sqlalchemy.orm import Session, aliased

# Import json lainnya

import logging

# Fungsi helper untuk memformat tanggal dengan aman
def json_format_date(date_value, date_format='%Y-%m-%d %H:%M:%S'):
    """
    Memformat nilai tanggal menjadi string sesuai format yang diberikan.
    
    Args:
        date_value: Nilai tanggal yang akan diformat (datetime atau string).
        date_format: Format string untuk output tanggal (default: '%Y-%m-%d %H:%M:%S').
    
    Returns:
        String yang diformat sesuai format, atau None jika nilai tidak valid.
    """
    # Periksa apakah nilai tanggal kosong atau string tidak valid
    if not date_value or str(date_value) in ['0000-00-00', '0000-00-00 00:00:00']:
        return None
    try:
        # Format nilai tanggal menggunakan format yang diberikan
        return date_value.strftime(date_format)
    except AttributeError:
        # Jika nilai bukan objek datetime, kembalikan None
        return None


async def json_data_timestamp(db: Session, data_row: dict = None) -> dict:
    if data_row is None:
        logging.error("data_row is None")
        return {}

    try:
        def format_datetime(value):
            """
            Helper function to format datetime.
            Handles '0000-00-00 00:00:00' and None values.
            """
            if value in [None, "0000-00-00 00:00:00"]:
                return None
            try:
                return value.strftime('%Y-%m-%d %H:%M:%S')
            except AttributeError:
                return None

        return {
            "created_by": data_row.created_by if hasattr(data_row, 'created_by') else None,
            "created_at": format_datetime(data_row.created_at if hasattr(data_row, 'created_at') else None),
            "updated_by": data_row.updated_by if hasattr(data_row, 'updated_by') else None,
            "updated_at": format_datetime(data_row.updated_at if hasattr(data_row, 'updated_at') else None),
            "deleted_by": data_row.deleted_by if hasattr(data_row, 'deleted_by') else None,
            "deleted_at": format_datetime(data_row.deleted_at if hasattr(data_row, 'deleted_at') else None),
            "revised": data_row.revised if hasattr(data_row, 'revised') else None,
        }
    except Exception as e:
        db.rollback()
        logging.error(f"Exception: {e}")
        return {}