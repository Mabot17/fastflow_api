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
from core.modules.master.produk.model.produk_model import ProdukModel
from core.modules.master.produk_group.model.produk_group_model import ProdukGroupModel
from core.modules.persediaan.penerimaan_barang.model.penerimaan_barang_model import PenerimaanBarangModel
from core.modules.persediaan.penerimaan_tagihan.model.penerimaan_tagihan_model import PenerimaanTagihanModel
from core.modules.transaksi.master_order_jual.model.master_order_jual_model import MasterOrderJualModel
from core.modules.transaksi.master_jual_produk.model.master_jual_produk_model import MasterJualProdukModel
from core.modules.users.schema.users_schema import UsersBaseSchema

# Import cek data model
from core.shared.check_data_model import (
    check_user_by_username,
    check_produk_group
)

def generate_pt_nobukti(db: Session, tanggal: date) -> str:
    # Dapatkan tahun dan bulan saat ini dalam format YYMM
    current_date = tanggal.strftime("%y%m")

    # Dapatkan nomor terakhir yang dihasilkan untuk tahun dan bulan ini
    last_record = db.query(PenerimaanTagihanModel.invoice_no_auto).filter(
        func.DATE_FORMAT(PenerimaanTagihanModel.invoice_tanggal, '%y%m') == current_date
    ).order_by(PenerimaanTagihanModel.invoice_no_auto.desc()).first()

    last_running_number = 1  # Default nomor urut jika tidak ada data
    if last_record and last_record.invoice_no_auto:
        # Ambil bagian nomor urut dari invoice_no_auto terakhir
        match = re.search(r'PT/\d{4}-\d{4}$', last_record.invoice_no_auto)
        if match:
            try:
                last_running_number = int(last_record.invoice_no_auto.split('-')[-1]) + 1
            except ValueError:
                print("Error: Gagal mengonversi nomor urut menjadi integer")
        else:
            print("Error: Format invoice_no_auto tidak sesuai, menggunakan default nomor urut 1")

    # Tambahkan nomor running ke format awal
    prefix = f"PT/{current_date}"
    running_number = f"{last_running_number:04d}"
    invoice_no_auto = f"{prefix}-{running_number}"

    return invoice_no_auto

def generate_terima_nobukti(db: Session, tanggal: date) -> str:
    # Dapatkan tahun dan bulan saat ini dalam format YYMM
    current_date = tanggal.strftime("%y%m")

    # Dapatkan nomor terakhir yang dihasilkan untuk tahun dan bulan ini
    last_record = db.query(PenerimaanBarangModel.terima_no).filter(
        func.DATE_FORMAT(PenerimaanBarangModel.terima_tanggal, '%y%m') == current_date
    ).order_by(PenerimaanBarangModel.terima_no.desc()).first()

    last_running_number = 1  # Default nomor urut jika tidak ada data
    if last_record and last_record.terima_no:
        # Ambil bagian nomor urut dari terima_no terakhir
        match = re.search(r'PB/\d{4}-\d{4}$', last_record.terima_no)
        if match:
            try:
                last_running_number = int(last_record.terima_no.split('-')[-1]) + 1
            except ValueError:
                print("Error: Gagal mengonversi nomor urut menjadi integer")
        else:
            print("Error: Format terima_no tidak sesuai, menggunakan default nomor urut 1")

    # Tambahkan nomor running ke format awal
    prefix = f"PB/{current_date}"
    running_number = f"{last_running_number:04d}"
    terima_no = f"{prefix}-{running_number}"

    return terima_no

async def generate_order_jual_nobukti(db: Session, tanggal: date, identity: UsersBaseSchema) -> str:
    current_date = tanggal.strftime("%y%m")
    prefix = f"OJ/{current_date}"

    # Ambil nomor terakhir berdasarkan prefix, urutan menurun
    last_record = db.query(MasterOrderJualModel.ojual_no).filter(
        func.DATE_FORMAT(MasterOrderJualModel.ojual_tanggal, '%y%m') == current_date,
        MasterOrderJualModel.ojual_no.like(f"{prefix}%")
    ).order_by(MasterOrderJualModel.ojual_no.desc()).first()

    # Tentukan nomor urut
    last_running_number = 1
    if last_record:
        match = re.search(r"-(\d+)$", last_record.ojual_no)
        if match:
            last_running_number = int(match.group(1)) + 1

    return f"{prefix}-{last_running_number:04d}"


async def generate_pos_nobukti(db: Session, tanggal: date, identity: UsersBaseSchema) -> str:
    current_date = tanggal.strftime("%y%m")
    data_user = await check_user_by_username(db, user_name=identity.user_name)
    prefix = f"{data_user.user_kode}/{current_date}"

    # Ambil nomor terakhir berdasarkan prefix, urutan menurun
    last_record = db.query(MasterJualProdukModel.jproduk_nobukti).filter(
        MasterJualProdukModel.jproduk_sumber == 'pos',
        func.DATE_FORMAT(MasterJualProdukModel.jproduk_tanggal, '%y%m') == current_date,
        MasterJualProdukModel.jproduk_nobukti.like(f"{prefix}%")
    ).order_by(MasterJualProdukModel.jproduk_nobukti.desc()).first()

    # Tentukan nomor urut
    last_running_number = 1
    if last_record:
        match = re.search(r"-(\d+)$", last_record.jproduk_nobukti)
        if match:
            last_running_number = int(match.group(1)) + 1

    return f"{prefix}-{last_running_number:04d}"

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

    return f"{prefix}{last_running_number:04d}"

