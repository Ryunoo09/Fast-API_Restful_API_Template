import logging
from sqlalchemy.orm import Session
from app.core.database import SessionLocal
from app.models.user import User
from app.models.post import Post
from app.models.comment import Comment

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Data dummy dari file create_tables.sql
# Semua password didefinisikan dengan hash bcrypt dari kata "password":
# $2b$12$4xJzHJvKe9N5m/aIkEqNy.KLOT3TlH8nnbu4BD9OAMt90RJWmeenC
USERS_DATA = [
    {
        "id": 1,
        "name": "Admin Ganteng",
        "email": "admin@email.com",
        "password": "$2b$12$4xJzHJvKe9N5m/aIkEqNy.KLOT3TlH8nnbu4BD9OAMt90RJWmeenC",
        "role": "admin",
    },
    {
        "id": 2,
        "name": "Admin Manis",
        "email": "admin2@email.com",
        "password": "$2b$12$4xJzHJvKe9N5m/aIkEqNy.KLOT3TlH8nnbu4BD9OAMt90RJWmeenC",
        "role": "admin",
    },
    {
        "id": 3,
        "name": "Budi Raharjo",
        "email": "budi@email.com",
        "password": "$2b$12$4xJzHJvKe9N5m/aIkEqNy.KLOT3TlH8nnbu4BD9OAMt90RJWmeenC",
        "role": "user",
    },
    {
        "id": 4,
        "name": "Siti Aminah",
        "email": "siti@email.com",
        "password": "$2b$12$4xJzHJvKe9N5m/aIkEqNy.KLOT3TlH8nnbu4BD9OAMt90RJWmeenC",
        "role": "user",
    },
    {
        "id": 5,
        "name": "Rakha Pratama",
        "email": "rakha@email.com",
        "password": "$2b$12$4xJzHJvKe9N5m/aIkEqNy.KLOT3TlH8nnbu4BD9OAMt90RJWmeenC",
        "role": "user",
    },
    {
        "id": 6,
        "name": "Bagus Wijaya",
        "email": "bagus@email.com",
        "password": "$2b$12$4xJzHJvKe9N5m/aIkEqNy.KLOT3TlH8nnbu4BD9OAMt90RJWmeenC",
        "role": "user",
    },
    {
        "id": 7,
        "name": "Joko Susilo",
        "email": "joko@email.com",
        "password": "$2b$12$4xJzHJvKe9N5m/aIkEqNy.KLOT3TlH8nnbu4BD9OAMt90RJWmeenC",
        "role": "user",
    },
]

POSTS_DATA = [
    {
        "id": 1,
        "title": "Aturan Aplikasi",
        "status": "published",
        "content": "Ini adalah peraturan platform kita.",
        "user_id": 1,
    },
    {
        "id": 2,
        "title": "Pengumuman Maintenance",
        "status": "draft",
        "content": "Maintenance akan dilakukan besok jam 12.",
        "user_id": 2,
    },
    {
        "id": 3,
        "title": "Tips Belajar Python",
        "status": "published",
        "content": "FastAPI sangat keren untuk backend dev.",
        "user_id": 3,
    },
    {
        "id": 4,
        "title": "Kisah Petualanganku",
        "status": "published",
        "content": "Saya pergi ke mendaki gunung.",
        "user_id": 4,
    },
    {
        "id": 5,
        "title": "Pengenalan Diri",
        "status": "draft",
        "content": "Halo, ini post pertama saya di platform.",
        "user_id": 5,
    },
    {
        "id": 6,
        "title": "Review Makanan",
        "status": "published",
        "content": "Nasi goreng di depan kampus sangat enak.",
        "user_id": 6,
    },
    {
        "id": 7,
        "title": "Buku Favorit 2026",
        "status": "published",
        "content": "Clean Code oleh Uncle Bob.",
        "user_id": 7,
    },
]

COMMENTS_DATA = [
    {"id": 1, "comment": "Sangat informatif admin!", "post_id": 1, "user_id": 3},
    {"id": 2, "comment": "Wah, saya harus bersiap-siap!", "post_id": 2, "user_id": 4},
    {"id": 3, "comment": "Betul sekali, fastapi jauh lebih cepat", "post_id": 3, "user_id": 5},
    {"id": 4, "comment": "Semangat mendaki mbak siti", "post_id": 4, "user_id": 3},
    {"id": 5, "comment": "Halo juga, salam kenal", "post_id": 5, "user_id": 2},
    {"id": 6, "comment": "Besok saya mau coba nasi gorengnya ah", "post_id": 6, "user_id": 7},
    {"id": 7, "comment": "Buku yang sangat melegenda di kalangan programmer", "post_id": 7, "user_id": 1},
]


def seed_db():
    db: Session = SessionLocal()
    try:
        # Bersihkan data lama dengan urutan yang aman dari Foreign Key constraint
        logger.info("Membersihkan data lama dari database...")
        db.query(Comment).delete()
        db.query(Post).delete()
        db.query(User).delete()
        db.commit()

        # Seed Users
        logger.info("Memasukkan data dummy users...")
        for user_dict in USERS_DATA:
            user = User(**user_dict)
            db.add(user)
        db.commit()

        # Seed Posts
        logger.info("Memasukkan data dummy posts...")
        for post_dict in POSTS_DATA:
            post = Post(**post_dict)
            db.add(post)
        db.commit()

        # Seed Comments
        logger.info("Memasukkan data dummy comments...")
        for comment_dict in COMMENTS_DATA:
            comment = Comment(**comment_dict)
            db.add(comment)
        db.commit()

        logger.info("Database berhasil di-seed!")

    except Exception as e:
        db.rollback()
        logger.error(f"Gagal melakukan seeding pada database: {e}")
        raise e
    finally:
        db.close()


if __name__ == "__main__":
    seed_db()
