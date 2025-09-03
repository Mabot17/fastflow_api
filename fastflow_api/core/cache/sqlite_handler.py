import sqlite3
from pathlib import Path
from typing import Any, Optional

# Lokasi database SQLite
DB_PATH = Path(__file__).parent / "cache.db"

class SQLiteHandler:
    def __init__(self):
        self.conn = sqlite3.connect(DB_PATH, check_same_thread=False)
        self.cursor = self.conn.cursor()
        self._create_table()  # Buat tabel saat objek diinisialisasi

    def _create_table(self):
        """Buat tabel jika belum ada"""
        self.cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS cache (
                key TEXT PRIMARY KEY,
                value TEXT,
                timestamp INTEGER DEFAULT (strftime('%s', 'now'))
            )
            """
        )
        self.conn.commit()

    def set(self, key: str, value: Any):
        """Simpan data ke cache"""
        self.cursor.execute(
            "INSERT OR REPLACE INTO cache (key, value) VALUES (?, ?)", (key, value)
        )
        self.conn.commit()

    def get(self, key: str) -> Optional[str]:
        """Ambil data dari cache"""
        self.cursor.execute("SELECT value FROM cache WHERE key = ?", (key,))
        result = self.cursor.fetchone()
        return result[0] if result else None

    def delete(self, key: str):
        """Hapus data dari cache"""
        self.cursor.execute("DELETE FROM cache WHERE key = ?", (key,))
        self.conn.commit()

    def clear(self):
        """Hapus semua data dalam cache"""
        self.cursor.execute("DELETE FROM cache")
        self.conn.commit()

# Inisialisasi handler
sqlite_handler = SQLiteHandler()


# # ROUTE LIST & SEARCH DATA JABATAN
# @routerProduk.get("", response_model=ProdukListSchema, responses=example_responses)
# async def get_all_produk(
#     http_request: Request,
#     request: ProdukRequestListSchema = Depends(ProdukRequestListSchema.as_form),
#     identity: UsersReqSchema = Depends(get_current_user),
#     db: Session = Depends(get_db),
# ):
#     try:
#         # Buat key cache dari semua parameter request (diurutkan supaya konsisten)
#         cache_key = f"produk:{json.dumps(request.model_dump(), sort_keys=True)}"

#         # Cek di cache SQLite
#         cached_data = sqlite_handler.get(cache_key)
#         if cached_data:
#             return JSONResponse(content=json.loads(cached_data), status_code=200)

#         # Jika tidak ada di cache, ambil dari database
#         daftar = await get_crud_daftar_produk(db=db, request=request)

#         if daftar.get("total_data"):
#             result = await show_success_list(
#                 http_request=http_request,
#                 data=daftar.get("data"),
#                 total_data=daftar.get("total_data"),
#                 page=request.page,
#                 results_per_page=request.results_per_page,
#                 is_paging=True,
#             )
#             # Simpan ke cache SQLite
#             sqlite_handler.set(cache_key, json.dumps(result))
#         else:
#             result = await show_not_found(http_request=http_request, status_code=404)

#         return JSONResponse(content=result, status_code=result["status"]["code"])

#     except Exception as e:
#         logging.error(f"Exception list_produk: {e}")
#         result = show_bad_response(error=str(e), http_request=http_request)
#         return JSONResponse(content=result)