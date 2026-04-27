-- ============================================================
-- SQL Script: Create Database & Tables for FastAPI Blog
-- Sesuai dengan model SQLAlchemy di folder app/models/
-- ============================================================

-- 1. Buat database blog (jika belum ada)
CREATE DATABASE IF NOT EXISTS `blog`;
USE `blog`;

-- ============================================================
-- 2. Tabel users (dari model: app/models/user.py)
-- Fields: id, name, email, password, role
-- ============================================================
CREATE TABLE IF NOT EXISTS `users` (
    `id` INT NOT NULL AUTO_INCREMENT,
    `name` VARCHAR(100) NOT NULL,
    `email` VARCHAR(50) NOT NULL,
    `password` VARCHAR(100) NOT NULL,
    `role` VARCHAR(20) NOT NULL DEFAULT 'user',
    PRIMARY KEY (`id`),
    UNIQUE KEY `ix_users_email` (`email`),
    KEY `ix_users_id` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- ============================================================
-- 3. Tabel posts (dari model: app/models/post.py)
-- Fields: id, title, status (draft/published), content, user_id
-- ============================================================
CREATE TABLE IF NOT EXISTS `posts` (
    `id` INT NOT NULL AUTO_INCREMENT,
    `title` VARCHAR(100) NOT NULL,
    `status` ENUM('draft', 'published') NOT NULL DEFAULT 'draft',
    `content` TEXT NOT NULL,
    `user_id` INT NOT NULL,
    PRIMARY KEY (`id`),
    KEY `ix_posts_id` (`id`),
    CONSTRAINT `fk_posts_user_id` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- ============================================================
-- 4. Tabel comments (dari model: app/models/comment.py)
-- Fields: id, comment, post_id, user_id
-- ============================================================
CREATE TABLE IF NOT EXISTS `comments` (
    `id` INT NOT NULL AUTO_INCREMENT,
    `comment` VARCHAR(250) NOT NULL,
    `post_id` INT NOT NULL,
    `user_id` INT NOT NULL,
    PRIMARY KEY (`id`),
    KEY `ix_comments_id` (`id`),
    KEY `ix_comments_post_id` (`post_id`),
    KEY `ix_comments_user_id` (`user_id`),
    CONSTRAINT `fk_comments_post_id` FOREIGN KEY (`post_id`) REFERENCES `posts` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT,
    CONSTRAINT `fk_comments_user_id` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- ============================================================
-- 5. Insert Data Dummy
-- Semua sandi (password) untuk user di bawah ini adalah: "password"
-- Hasil hash passlib.bcrypt dari kata "password":
-- $2b$12$4xJzHJvKe9N5m/aIkEqNy.KLOT3TlH8nnbu4BD9OAMt90RJWmeenC
-- ============================================================

-- Insert 7 Dummy Users (2 Admin, 5 User)
INSERT INTO `users` (`id`, `name`, `email`, `password`, `role`) VALUES
(1, 'Admin Ganteng', 'admin@email.com', '$2b$12$4xJzHJvKe9N5m/aIkEqNy.KLOT3TlH8nnbu4BD9OAMt90RJWmeenC', 'admin'),
(2, 'Admin Manis', 'admin2@email.com', '$2b$12$4xJzHJvKe9N5m/aIkEqNy.KLOT3TlH8nnbu4BD9OAMt90RJWmeenC', 'admin'),
(3, 'Budi Raharjo', 'budi@email.com', '$2b$12$4xJzHJvKe9N5m/aIkEqNy.KLOT3TlH8nnbu4BD9OAMt90RJWmeenC', 'user'),
(4, 'Siti Aminah', 'siti@email.com', '$2b$12$4xJzHJvKe9N5m/aIkEqNy.KLOT3TlH8nnbu4BD9OAMt90RJWmeenC', 'user'),
(5, 'Rakha Pratama', 'rakha@email.com', '$2b$12$4xJzHJvKe9N5m/aIkEqNy.KLOT3TlH8nnbu4BD9OAMt90RJWmeenC', 'user'),
(6, 'Bagus Wijaya', 'bagus@email.com', '$2b$12$4xJzHJvKe9N5m/aIkEqNy.KLOT3TlH8nnbu4BD9OAMt90RJWmeenC', 'user'),
(7, 'Joko Susilo', 'joko@email.com', '$2b$12$4xJzHJvKe9N5m/aIkEqNy.KLOT3TlH8nnbu4BD9OAMt90RJWmeenC', 'user');

-- Insert 7 Dummy Posts
INSERT INTO `posts` (`id`, `title`, `status`, `content`, `user_id`) VALUES
(1, 'Aturan Aplikasi', 'published', 'Ini adalah peraturan platform kita.', 1),
(2, 'Pengumuman Maintenance', 'draft', 'Maintenance akan dilakukan besok jam 12.', 2),
(3, 'Tips Belajar Python', 'published', 'FastAPI sangat keren untuk backend dev.', 3),
(4, 'Kisah Petualanganku', 'published', 'Saya pergi ke mendaki gunung.', 4),
(5, 'Pengenalan Diri', 'draft', 'Halo, ini post pertama saya di platform.', 5),
(6, 'Review Makanan', 'published', 'Nasi goreng di depan kampus sangat enak.', 6),
(7, 'Buku Favorit 2026', 'published', 'Clean Code oleh Uncle Bob.', 7);

-- Insert 7 Dummy Comments
INSERT INTO `comments` (`id`, `comment`, `post_id`, `user_id`) VALUES
(1, 'Sangat informatif admin!', 1, 3),
(2, 'Wah, saya harus bersiap-siap!', 2, 4),
(3, 'Betul sekali, fastapi jauh lebih cepat', 3, 5),
(4, 'Semangat mendaki mbak siti', 4, 3),
(5, 'Halo juga, salam kenal', 5, 2),
(6, 'Besok saya mau coba nasi gorengnya ah', 6, 7),
(7, 'Buku yang sangat melegenda di kalangan programmer', 7, 1);
