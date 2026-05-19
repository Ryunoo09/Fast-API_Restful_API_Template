from fastapi import status


class TestPostEndpoints:
    """Tests for Post API endpoints."""

    def test_create_post_unauthorized(self, client):
        """Skenario 401: Mengetes endpoint tanpa header Authorization."""
        response = client.post(
            "/api/v1/posts/",
            json={"title": "Test Title", "content": "Test Content", "user_id": 1},
        )
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_create_post_success(self, client, token_headers):
        """Skenario 201: Membuat data dengan token JWT."""
        response = client.post(
            "/api/v1/posts/",
            json={"title": "My New Post", "content": "This is a test content", "user_id": 1},
            headers=token_headers,
        )
        assert response.status_code == status.HTTP_201_CREATED
        data = response.json()
        assert data["title"] == "My New Post"
        assert "id" in data

    def test_update_post_forbidden(self, client, token_headers):
        """Skenario 403: User A mencoba mengedit data milik User B."""
        # 1. Buat User B (user dummy kedua)
        client.post(
            "/api/v1/users/",
            json={
                "name": "User B",
                "email": "userb@example.com",
                "password": "password123",
            },
        )
        # Login sebagai User B
        login_res = client.post(
            "/api/v1/auth/login", data={"username": "userb@example.com", "password": "password123"}
        )
        token_b = login_res.json()["data"]["access_token"]
        headers_b = {"Authorization": f"Bearer {token_b}"}

        # 2. User B membuat Post
        post_res = client.post(
            "/api/v1/posts/",
            json={"title": "User B Post", "content": "Content B", "user_id": 2},
            headers=headers_b,
        )
        post_id = post_res.json()["id"]

        # 3. User A (menggunakan token_headers dari fixture) mencoba mengedit post milik User B
        update_res = client.put(
            f"/api/v1/posts/{post_id}",
            json={"title": "Hacked by User A", "content": "Hacked content"},
            headers=token_headers,
        )
        assert update_res.status_code == status.HTTP_403_FORBIDDEN

    def test_get_post_not_found(self, client, token_headers):
        """Skenario 404: Request ke ID data yang tidak ada."""
        response = client.get("/api/v1/posts/9999", headers=token_headers)
        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_get_posts_only_own_data(self, client, token_headers):
        """Skenario: Menampilkan semua data post milik user yang sedang login saja."""
        # 1. User A (token_headers) membuat 1 post
        client.post(
            "/api/v1/posts/",
            json={"title": "User A Post", "content": "My content", "user_id": 1},
            headers=token_headers,
        )

        # 2. Registrasi dan Login User B
        client.post(
            "/api/v1/users/",
            json={
                "name": "User B",
                "email": "userb@example.com",
                "password": "password123",
            },
        )
        login_res = client.post(
            "/api/v1/auth/login", data={"username": "userb@example.com", "password": "password123"}
        )
        token_b = login_res.json()["data"]["access_token"]
        headers_b = {"Authorization": f"Bearer {token_b}"}

        # User B membuat 2 posts
        client.post(
            "/api/v1/posts/",
            json={"title": "User B Post 1", "content": "Content B1", "user_id": 2},
            headers=headers_b,
        )
        client.post(
            "/api/v1/posts/",
            json={"title": "User B Post 2", "content": "Content B2", "user_id": 2},
            headers=headers_b,
        )

        # 3. User A meminta semua posts (GET /)
        response_a = client.get("/api/v1/posts/", headers=token_headers)
        assert response_a.status_code == status.HTTP_200_OK
        data_a = response_a.json()
        
        # User A harusnya hanya melihat 1 post miliknya sendiri (bukan milik User B)
        assert data_a["total"] == 1
        assert data_a["posts"][0]["title"] == "User A Post"

    def test_get_post_by_id_success(self, client, token_headers):
        """Skenario: Menampilkan data post berdasarkan ID yang sukses (milik sendiri)."""
        # 1. Buat post baru
        create_res = client.post(
            "/api/v1/posts/",
            json={"title": "Target Post", "content": "Important info", "user_id": 1},
            headers=token_headers,
        )
        post_id = create_res.json()["id"]

        # 2. Ambil post berdasarkan ID
        response = client.get(f"/api/v1/posts/{post_id}", headers=token_headers)
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data["id"] == post_id
        assert data["title"] == "Target Post"

    def test_get_post_by_id_forbidden(self, client, token_headers):
        """Skenario 403: User A mencoba melihat detail post milik User B yang terproteksi."""
        # 1. Buat User B
        client.post(
            "/api/v1/users/",
            json={
                "name": "User B",
                "email": "userb@example.com",
                "password": "password123",
            },
        )
        login_res = client.post(
            "/api/v1/auth/login", data={"username": "userb@example.com", "password": "password123"}
        )
        token_b = login_res.json()["data"]["access_token"]
        headers_b = {"Authorization": f"Bearer {token_b}"}

        # User B membuat post
        create_res = client.post(
            "/api/v1/posts/",
            json={"title": "Private Post B", "content": "Secret content", "user_id": 2},
            headers=headers_b,
        )
        post_id = create_res.json()["id"]

        # 2. User A mencoba melihat detail post milik User B → Harus 403 Forbidden
        response = client.get(f"/api/v1/posts/{post_id}", headers=token_headers)
        assert response.status_code == status.HTTP_403_FORBIDDEN

