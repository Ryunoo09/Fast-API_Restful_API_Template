from fastapi import status


class TestUserEndpoints:
    """Tests for User API endpoints."""

    def test_create_user(self, client):
        """Test creating a new user."""
        response = client.post(
            "/api/v1/users/",
            json={
                "username": "testuser",
                "email": "test@example.com",
                "password": "testpassword123",
                "full_name": "Test User",
            },
        )
        assert response.status_code == status.HTTP_201_CREATED
        data = response.json()
        assert data["username"] == "testuser"
        assert data["email"] == "test@example.com"
        assert "password" not in data

    def test_get_users(self, client):
        """Test getting all users."""
        response = client.get("/api/v1/users/")
        assert response.status_code == status.HTTP_200_OK

    def test_get_user_not_found(self, client):
        """Test getting a non-existent user returns 404."""
        response = client.get("/api/v1/users/999")
        assert response.status_code == status.HTTP_404_NOT_FOUND
