# FastAPI Blog API (Chapter 7 & 8 Concept Implementation)

Proyek FastAPI dengan pola **Clean Architecture** yang mengimplementasikan konsep-konsep dari Chapter 7 dan Chapter 8 (sebelumnya berbasis Lumen/Laravel) ke dalam ekosistem Python modern.

## ✨ Fitur Utama (Chapter 7 Adaptation)

- **API Versioning**: Menggunakan prefix `/api/v1/` untuk skalabilitas (menggantikan Dingo API).
- **JWT Authentication**: Mekanisme login aman menggunakan `bcrypt` dan JWT (`python-jose`).
- **Token Refresh Mechanism**: Penukaran `refresh_token` menjadi `access_token` baru tanpa login ulang.
- **Token Invalidation (Logout)**: Pembatalan token melalui sistem *Blacklist* (In-memory/Redis).
- **Rate Limiting (Throttling)**: Pencegahan Brute Force dan Spam menggunakan `slowapi` (contoh: maksimal 20 request/menit untuk login).
- **Pydantic Transformers**: Transformasi data dari Database (SQLAlchemy) menjadi JSON yang aman dan bersih, menyembunyikan field sensitif seperti password (menggantikan Fractal Transformers).
- **Standardized Response**: Format response yang seragam `{ "message": "...", "data": {...} }` untuk memudahkan konsumsi oleh Frontend.
- **Automated Testing (Chapter 8)**: Sistem pengujian otomatis menggunakan Pytest dengan database terisolasi (SQLite in-memory), mencakup skenario 401, 201, 403, dan 404.

## 📁 Struktur Folder

```text
fastapi_python/
├── app/
│   ├── main.py                  # Entry point & SlowAPI middleware setup
│   ├── core/                    # Konfigurasi & Infrastruktur
│   │   ├── config.py            # Setting Environment & API_V1_STR
│   │   ├── database.py          # Koneksi SQLAlchemy
│   │   ├── rate_limit.py        # Konfigurasi SlowAPI (Throttling)
│   │   ├── security.py          # JWT Generation & Password Hashing
│   │   └── token_blacklist.py   # JWT Blacklisting (Logout handling)
│   ├── models/                  # SQLAlchemy ORM Models (Tabel DB)
│   │   ├── user.py
│   │   ├── post.py
│   │   └── comment.py
│   ├── schemas/                 # Pydantic Schemas (Data Transformers)
│   │   ├── auth.py
│   │   ├── user.py
│   │   ├── post.py
│   │   └── comment.py
│   ├── repositories/            # Data Access Layer (Query DB)
│   │   └── user_repository.py
│   ├── services/                # Business Logic Layer
│   │   └── post_service.py
│   ├── api/                     # API Routes & Endpoints
│   │   ├── dependencies.py      # Route Protection (get_current_user)
│   │   └── v1/
│   │       ├── router.py        # Central Router
│   │       └── endpoints/
│   │           ├── auth.py      # Login, Register, Refresh, Logout
│   │           ├── users.py
│   │           ├── posts.py
│   │           └── comments.py
│   └── utils/                   # Helper Functions
│       ├── exceptions.py        # Global Exception Handlers
│       └── response.py          # Standardized Response Helper
├── tests/                       # 🧪 Automated Testing (Chapter 8)
│   ├── __init__.py
│   ├── conftest.py              # Fixtures: db_session, client, token_headers
│   ├── test_auth.py             # Pengujian endpoint autentikasi
│   ├── test_posts.py            # Pengujian endpoint posts (401, 201, 403, 404)
│   └── test_users.py            # Pengujian endpoint users
├── .env                         # Environment variables (Database & JWT Secret)
├── .env.test                    # Environment variables khusus testing
├── pytest.ini                   # Konfigurasi Pytest
├── requirements.txt
└── README.md
```

## 🚀 Quick Start

```bash
# 1. Aktivasi virtual environment
python -m venv venv
venv\Scripts\activate        # Windows
source venv/bin/activate     # Mac/Linux

# 2. Install dependencies
pip install -r requirements.txt

# 3. Setup Database (.env)
# Pastikan MySQL berjalan dan sesuai dengan konfigurasi di .env

# 4. Jalankan server
uvicorn app.main:app --reload

# 5. Buka Dokumentasi Interaktif
# Swagger UI: http://127.0.0.1:8000/docs
```

## 📚 API Endpoints Utama

### 🔐 Autentikasi (Rate Limited)
| Method | URL | Deskripsi |
|--------|-----|-----------|
| `POST` | `/api/v1/auth/register` | Daftar user baru |
| `POST` | `/api/v1/auth/login` | Login (Mengembalikan Access & Refresh Token) |
| `POST` | `/api/v1/auth/refresh` | Dapatkan Access Token baru menggunakan Refresh Token |
| `DELETE` | `/api/v1/auth/logout` | Logout (Blacklist Token saat ini) |
| `POST` | `/api/v1/auth/reset-password`| Ubah password (Membutuhkan Auth) |

### 📝 Posts (Protected)
| Method | URL | Deskripsi |
|--------|-----|-----------|
| `GET` | `/api/v1/posts/` | List postingan (User: miliknya sendiri, Admin: semua) |
| `GET` | `/api/v1/posts/{id}` | Detail postingan |
| `POST` | `/api/v1/posts/` | Buat postingan baru |
| `PUT` | `/api/v1/posts/{id}` | Update postingan |
| `DELETE` | `/api/v1/posts/{id}` | Hapus postingan (Hanya Admin) |

### 💬 Comments (Protected)
| Method | URL | Deskripsi |
|--------|-----|-----------|
| `GET` | `/api/v1/comments/` | List komentar |
| `POST` | `/api/v1/comments/` | Tambah komentar pada post |
| `DELETE` | `/api/v1/comments/{id}` | Hapus komentar (Pembuat / Admin) |

---

## 🧪 Automated Testing (Chapter 8)

Proyek ini mengimplementasikan sistem **Automated Testing** menggunakan **Pytest** sebagai adaptasi dari konsep Bab 8 pada Laravel/Lumen. Pengujian dilakukan secara terisolasi menggunakan **SQLite in-memory**, sehingga tidak mengganggu data pada database MySQL production.

### Cara Menjalankan Pengujian

```bash
# Pastikan virtual environment sudah aktif
.\venv\Scripts\activate

# 1. Jalankan semua test sekaligus (Standard Verbose)
pytest tests/ -v

# 2. Jalankan test pada file tertentu saja
pytest tests/test_posts.py -v

# 3. Jalankan test dengan LOG LENGKAP & PRINT LIVE (Tanpa capture stdout)
pytest tests/ -v -s

# 4. Jalankan test dengan LIVE LOGGING CLI dari FastAPI (Menampilkan log level INFO ke terminal)
pytest tests/ -v -o log_cli=true --log-cli-level=INFO

# 5. Jalankan test dan simpan SELURUH LOG LENGKAP ke dalam berkas file log
pytest tests/ -v --log-file=test_output.log --log-file-level=DEBUG
```

### 📋 Detail Opsi Pengujian & Logging

Untuk membantu proses pelacakan bug atau pemeriksaan alur request (*debugging*), Anda dapat memanfaatkan fitur perekaman log dari Pytest dengan opsi berikut:

* **Opsi `-s` atau `--capture=no`**: Secara *default*, Pytest akan menahan semua *output* standar seperti `print()` atau pesan logger yang dihasilkan selama pengujian. Dengan menambahkan opsi `-s`, semua pesan log dan perintah cetak (`print()`) akan langsung ditampilkan di terminal secara *real-time* sewaktu test berjalan.
* **Opsi `-o log_cli=true --log-cli-level=INFO`**: Opsi ini akan memaksa Pytest mengaktifkan fitur CLI Logging. Semua log aplikasi FastAPI (seperti log koneksi database SQLAlchemy, auth event, router access, dll.) dengan tingkatan level `INFO` ke atas akan dicetak langsung ke konsol terminal.
* **Opsi `--log-file=test_output.log --log-file-level=DEBUG`**: Berfungsi untuk mengekspor seluruh aktivitas log pengujian secara komprehensif ke dalam berkas log eksternal bernama `test_output.log`. Tingkatan level diatur ke `DEBUG` agar Anda mendapatkan rincian informasi terdalam dari sistem untuk keperluan *troubleshooting*.

### Skenario Pengujian yang Diimplementasikan

| No. | Skenario | File | HTTP Code |
|:---:|---|---|:---:|
| 1 | Login berhasil mendapatkan JWT token | `test_auth.py` | 200 OK |
| 2 | Login dengan password salah | `test_auth.py` | 401 Unauthorized |
| 3 | Akses endpoint tanpa token JWT | `test_posts.py` | 401 Unauthorized |
| 4 | Buat post dengan token JWT yang valid | `test_posts.py` | 201 Created |
| 5 | User A mencoba edit post milik User B | `test_posts.py` | 403 Forbidden |
| 6 | Akses post dengan ID yang tidak ada | `test_posts.py` | 404 Not Found |
| 7 | Registrasi user baru | `test_users.py` | 201 Created |
| 8 | Ambil daftar semua user | `test_users.py` | 200 OK |
| 9 | Ambil user dengan ID yang tidak ada | `test_users.py` | 404 Not Found |

### Infrastruktur Testing

Sistem testing dibangun di atas file `tests/conftest.py` yang menyediakan tiga fixture utama:

- **`db_session`**: Membuat ulang skema database (create & drop tables) untuk setiap fungsi test, memastikan isolasi data yang sempurna.
- **`client`**: Menyediakan `TestClient` dari FastAPI dengan database di-override ke SQLite in-memory, serta mencegah koneksi ke MySQL production saat startup.
- **`token_headers`**: Mensimulasikan proses registrasi dan login untuk menghasilkan JWT token yang siap digunakan sebagai header `Authorization` pada test case yang membutuhkan autentikasi.

---
*Proyek ini dirancang untuk menunjukkan bagaimana pola desain dari framework PHP (Lumen/Laravel) dapat diterjemahkan ke dalam arsitektur Python FastAPI yang modern, asinkron, dan efisien.*
