# FastAPI Blog API (Chapter 7 Concept Implementation)

Proyek FastAPI dengan pola **Clean Architecture** yang mengimplementasikan konsep-konsep dari Chapter 7 (sebelumnya berbasis Lumen/Laravel) ke dalam ekosistem Python modern.

## ✨ Fitur Utama (Chapter 7 Adaptation)

- **API Versioning**: Menggunakan prefix `/api/v1/` untuk skalabilitas (menggantikan Dingo API).
- **JWT Authentication**: Mekanisme login aman menggunakan `bcrypt` dan JWT (`python-jose`).
- **Token Refresh Mechanism**: Penukaran `refresh_token` menjadi `access_token` baru tanpa login ulang.
- **Token Invalidation (Logout)**: Pembatalan token melalui sistem *Blacklist* (In-memory/Redis).
- **Rate Limiting (Throttling)**: Pencegahan Brute Force dan Spam menggunakan `slowapi` (contoh: maksimal 20 request/menit untuk login).
- **Pydantic Transformers**: Transformasi data dari Database (SQLAlchemy) menjadi JSON yang aman dan bersih, menyembunyikan field sensitif seperti password (menggantikan Fractal Transformers).
- **Standardized Response**: Format response yang seragam `{ "message": "...", "data": {...} }` untuk memudahkan konsumsi oleh Frontend.

## 📁 Struktur Folder

```
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
├── .env                         # Environment variables (Database & JWT Secret)
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
*Proyek ini dirancang untuk menunjukkan bagaimana pola desain dari framework PHP (Lumen/Laravel) dapat diterjemahkan ke dalam arsitektur Python FastAPI yang modern, asinkron, dan efisien.*
