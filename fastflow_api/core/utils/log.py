import os
import logging
from core.config import config
import sys
from core import config
from sqlalchemy.dialects import mysql

logging.getLogger("boto").setLevel(logging.CRITICAL)
logging.getLogger("boto3").setLevel(logging.CRITICAL)
logging.getLogger("botocore").setLevel(logging.CRITICAL)


def setup_custom_logger(name: str, file_name: str = "default.log"):
    formatter = logging.Formatter(
        fmt="%(asctime)s - [%(levelname)s]%(filename)s:%(lineno)d > %(message)s"
    )

    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)

    if not logger.handlers:
        # 🔧 Buat folder log
        log_dir = os.path.join(config.UPLOAD_FOLDER, "logs")
        os.makedirs(log_dir, exist_ok=True)

        # 📝 File handler sesuai file_name
        file_path = os.path.join(log_dir, file_name)
        file_handler = logging.FileHandler(file_path)
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)

        # 🖥️ Console handler
        console_handler = logging.StreamHandler(stream=sys.stdout)
        console_handler.setFormatter(formatter)
        logger.addHandler(console_handler)

    logger.propagate = False
    return logger

def log_mysql_query(result):

    """
        # Contoh Penggunaan
        qr_data = (
            query.order_by(produkModel.produk_id)
            .limit(request.results_per_page)
            .offset(start_from(request.page, request.results_per_page))
        )
        result = (qr_data.all())
        sql_query = log_mysql_query(qr_data)
        print(sql_query)
    """
    # Mengambil query SQL dari SQLAlchemy
    sql_query = str(result.statement)
    
    # Ganti tanda kutip ganda dengan backtick untuk kompatibilitas MySQL
    sql_query_mysql = sql_query.replace('"', '`')
    
    # Kembalikan query SQL yang sudah disesuaikan
    return sql_query_mysql


def log_mysql_query_raw(query):
    """
        Render query SQLAlchemy menjadi query SQL mentah (raw) dengan nilai parameter.

        ### Cara Pemakaian
        query = db.query(MasterJualProdukModel.jproduk_nobukti).filter(
            MasterJualProdukModel.jproduk_sumber == 'pos',
            func.DATE_FORMAT(MasterJualProdukModel.jproduk_tanggal, '%y%m') == current_date,
            MasterJualProdukModel.jproduk_nobukti.like(f"{prefix}-%")
        ).order_by(MasterJualProdukModel.jproduk_nobukti.desc())

        # DEBUG: tampilkan SQL mentah
        raw_sql = log_mysql_query_raw(query)
        print(f"[DEBUG SQL] Query MySQL: {raw_sql}")

        ### eksekusi query
        last_record = query.first()
    """
    try:
        compiled = query.statement.compile(dialect=mysql.dialect(), compile_kwargs={"literal_binds": True})
        return str(compiled)
    except Exception as e:
        return f"[ERROR] Gagal log SQL: {e}"