# ⚡ FastFlow ERP_API

**FastFlow** adalah arsitektur backend berbasis **FastAPI** yang dirancang modular dan scalable untuk kebutuhan sistem ERP.  
Project ini menggunakan pendekatan layered architecture: `schema`, `router`, `crud`, `model`, serta pembagian utilitas dan modul per fitur.

---

## 📦 Requirements

- Python `3.11.7`
- [Poetry](https://python-poetry.org/) (install via pip)
- MySQL `8.4+`

---

## 🔧 Instalasi dan Menjalankan Aplikasi

```bash
# 1. Clone repository
git clone https://github.com/username/fastflow_api.git

# 2. Masuk ke direktori proyek
cd fastflow_api

# 3. Install dependensi
poetry lock
poetry install

# 4. Menjalankan server pengembangan
poetry run uvicorn main:app --host 127.0.0.1 --port 8001 --reload
```

---

## 🔐 Konfigurasi Environment

1. Buat file `.env` di:
   ```
   root/fastflow_api/core/.env
   ```

2. Salin isi dari:
   ```
   root/fastflow_api/core/.env.example
   ```

3. Sesuaikan konfigurasi `.env` untuk:
   - `DATABASE_URL`
   - `SECRET_KEY`
   - Konfigurasi lainnya sesuai kebutuhan aplikasi

---

## 🧩 Struktur Folder Utama (FastFlow Architecture)

```plaintext
.
├── fastflow_api/                    # Backend utama API
│   ├── core/
│   │   ├── router/
│   │   │   ├── api_router.py         # Pendaftaran semua router endpoint API
│   │   │   └── api_metadata.py       # Metadata untuk dokumentasi Swagger & Redoc
│   │   │
│   │   ├── modules/                  # Modul-modul utama berdasarkan fitur
│   │   │   └── nama_modul/
│   │   │       ├── schema/           # Pydantic model (request/response)
│   │   │       ├── router/           # Route untuk modul
│   │   │       ├── model/            # SQLAlchemy models (ORM)
│   │   │       └── crud/             # Akses database dan logika CRUD
│   │   │
│   │   ├── shared/                   # Konfigurasi global & objek bersama (DB, auth, dll)
│   │   ├── utils/                    # Layanan tambahan: plugins, helpers, services, dll
│   │   ├── .env                      # File environment variabel (JANGAN di-push)
│   │   └── .env.example              # Template konfigurasi environment
│
├── fastflow_statics/
│   └── sav_file/             # Folder penyimpanan file statis: laporan, hasil export
│
├── fastflow_updatedb/
│   └── *.sql                 # File SQL untuk pembaruan struktur database
│
└── README.md                 # Dokumentasi ini
```

---

## 🌐 Endpoint & Dokumentasi

- Swagger UI: [http://127.0.0.1:8001/docs](http://127.0.0.1:8001/docs)
- Redoc: [http://127.0.0.1:8001/redoc](http://127.0.0.1:8001/redoc)
- Rapidoc: [http://127.0.0.1:8001/rapidoc](http://127.0.0.1:8001/rapidoc)

> Dokumentasi otomatis terdaftar dari `api_router.py` & dikelola via `api_metadata.py`

---

## 🛠️ Fitur Kunci FastFlow

- 🔁 **Modular:** Penambahan modul baru hanya perlu tambah folder di `modules/`
- 🧱 **Terpisah:** Schema, router, model, crud semua dipisahkan per fungsi
- 🔄 **Auto-routing:** Semua router dapat diregistrasi otomatis di `api_router.py`
- 🔐 **Flexible Config:** `.env` lengkap untuk setting DB, secret, port, mode, dll
- 🧩 **Shared Layer:** Cocok untuk reusable global function, validasi, dan wrapper
- 🔧 **Utils Layer:** Tempat plugin, file service, tools encryption, dan kebutuhan khusus

---

## 🤝 Kontribusi

Kami terbuka untuk kontribusi dan kolaborasi.  
Langkah kontribusi:

1. Fork repositori ini
2. Buat branch baru (`fitur/nama-fitur`)
3. Commit perubahan dan push
4. Buat Pull Request

---

## 💬 Kontak

Untuk pertanyaan atau kerja sama: **[masrifan26@gmail.com]**

---

## ✨ Motto

> Harapan adalah doa.  
> Dibangun oleh **Mabot17** ✊