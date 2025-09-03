import json
from typing import Optional
from ..config import UPLOAD_FOLDER
from datetime import datetime

#  pengganti schema static, karena sangat merepotkan menambahkan satu per satu key
def parse_object_to_dict(obj):
    # Mendapatkan semua atribut dari objek
    obj_dict = vars(obj)
    # Filter atribut yang dapat di-serialize
    serializable_attributes = {key: value for key, value in obj_dict.items() if is_serializable(value)}
    return serializable_attributes

def is_serializable(value):
    try:
        # Mencoba mengonversi nilai ke JSON
        json.dumps(value)
        return True
    except (TypeError, OverflowError):
        return False
    
def parse_jam(jam_str):
    if not jam_str:
        return 0
    jam, menit = map(int, str(jam_str).split(':'))
    return jam * 60 + menit

def jam_format(total_menit):
    if not total_menit:
        return "00:00"
    jam = total_menit // 60
    menit = total_menit % 60
    return f"{jam:02}:{menit:02}"

    
# Fungsi untuk menghasilkan parsing URI gambar
def generate_image_uri(filename: Optional[str], bucket: Optional[str], region: Optional[str], path: Optional[str]) -> Optional[str]:
    if filename and bucket:
        return f"https://{bucket}.s3.{region}.amazonaws.com{path}/{filename}"
    else:
        return f"{UPLOAD_FOLDER}/{filename}"
    
def decrypt_query(query, params):
    """
    Fungsi untuk menggantikan parameter dalam query dengan nilai aktual dari params
    dan menghasilkan query SQL yang utuh.
    
    :param query: Query dalam format SQL dengan placeholder (misal :parameter)
    :param params: Dictionary berisi parameter dan nilai yang akan digantikan ke dalam query
    
    :return: Query SQL yang sudah lengkap dengan nilai parameter
    """
    query_str = str(query)  # Mengonversi TextClause ke string
    
    for key, value in params.items():
        # Cek apakah tipe data nilai adalah string
        if isinstance(value, str):
            # Mengganti :key dengan value, mengapit nilai string dengan tanda kutip
            query_str = query_str.replace(f":{key}", f"'{value}'")
        elif isinstance(value, datetime):
            # Jika nilai adalah datetime, konversi menjadi format tanggal yang valid
            query_str = query_str.replace(f":{key}", f"'{value.strftime('%Y-%m-%d')}'")
        else:
            # Jika bukan string atau datetime, langsung mengganti dengan nilai
            query_str = query_str.replace(f":{key}", str(value))
    
    return query_str