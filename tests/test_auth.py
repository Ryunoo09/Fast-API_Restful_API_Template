from fastapi import status


class TestAuthEndpoints:
    """Tests for Auth API endpoints."""

    def test_login_success(self, client):
        """Test login to get access token."""
        # Create a user first
        client.post(
            "/api/v1/users/",
            json={
                "name": "Auth User",
                "email": "authuser@example.com",
                "password": "password123",
            },
        )
        
        # Login
        response = client.post(
            "/api/v1/auth/login",
            data={"username": "authuser@example.com", "password": "password123"},
        )
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert "access_token" in data["data"]
        assert data["data"]["token_type"] == "bearer"

    def test_login_wrong_password(self, client):
        """Test login with incorrect password."""
        # Create a user first
        client.post(
            "/api/v1/users/",
            json={
                "name": "Auth User 2",
                "email": "authuser2@example.com",
                "password": "password123",
            },
        )
        
        # Login with wrong password
        response = client.post(
            "/api/v1/auth/login",
            data={"username": "authuser2@example.com", "password": "wrongpassword"},
        )
        assert response.status_code == status.HTTP_401_UNAUTHORIZED
