import pytest
from fastapi.testclient import TestClient


class TestAuthentication:
    @pytest.fixture
    def client(self) -> TestClient:
        """
        Test client for integration tests.
        """
        from main import get_application

        app = get_application()
        client = TestClient(app, base_url="http://testserver")
        return client

    def test_register_user(self, client):
        """
        Test the /register endpoint.
        """
        response = client.post(
            "/v1/register",
            json={"email": "testuser@test.com", "password": "testpass", "name": "Test", "role": "user"},
        )
        assert response.status_code == 200
        json_response = response.json()
        assert "message" in json_response
        assert json_response["message"] == "User registered successfully."

    def test_register_user_already_exists(self, client):
        """
        Test /register endpoint when user already exists.
        """
        client.post(
            "/v1/register",
            json={"email": "testuser@test.com", "password": "testpass", "name": "Test", "role": "user"},
        )
        response = client.post(
            "/v1/register",
            json={"email": "testuser@test.com", "password": "testpass", "name": "Test", "role": "user"},
        )
        assert response.status_code == 400
        json_response = response.json()
        assert "detail" in json_response
        assert json_response["detail"] == "User already exists."

    def test_login_user(self, client):
        """
        Test the /login endpoint.
        """
        client.post(
            "/v1/register",
            json={"email": "testlogin@test.com", "password": "testpass", "name": "Test", "role": "user"},
        )
        response = client.post(
            "/v1/login", params={"email": "testlogin@test.com", "password": "testpass"}
        )
        assert response.status_code == 200
        json_response = response.json()
        assert "access_token" in json_response
        assert json_response["token_type"] == "bearer"

    def test_login_user_invalid_credentials(self, client):
        """
        Test /login with invalid credentials.
        """
        response = client.post(
            "/v1/login", params={"email": "nonexistent@test.com", "password": "wrongpass"}
        )
        assert response.status_code == 404
        json_response = response.json()
        assert "detail" in json_response
        assert json_response["detail"] == "User not found."

    def test_list_users_admin(self, client):
        """
        Test the /users endpoint with an admin user.
        """
        client.post(
            "/v1/register",
            json={"email": "admin@test.com", "password": "adminpass", "name": "Admin", "role": "admin"},
        )
        response = client.post(
            "/v1/login", params={"email": "admin@test.com", "password": "adminpass"}
        )
        token = response.json().get("access_token")

        headers = {"Authorization": f"Bearer {token}"}
        response = client.get("/v1/users", headers=headers)
        assert response.status_code == 200
        json_response = response.json()
        assert "users" in json_response

    def test_list_users_non_admin(self, client):
        """
        Test the /users endpoint with a non-admin user.
        """
        client.post(
            "/v1/register",
            json={"email": "user@test.com", "password": "userpass", "name": "User", "role": "user"},
        )
        response = client.post(
            "/v1/login", params={"email": "user@test.com", "password": "userpass"}
        )
        token = response.json().get("access_token")

        headers = {"Authorization": f"Bearer {token}"}
        response = client.get("/v1/users", headers=headers)
        assert response.status_code == 403
        json_response = response.json()
        assert "detail" in json_response
        assert json_response["detail"] == "Not enough permissions. Admin role required"

    def test_logout_user(self, client):
        """
        Test the /logout endpoint.
        """
        client.post(
            "/v1/register",
            json={"email": "logoutuser@test.com", "password": "logoutpass", "name": "Logout", "role": "user"},
        )
        response = client.post(
            "/v1/login", params={"email": "logoutuser@test.com", "password": "logoutpass"}
        )
        token = response.json().get("access_token")

        headers = {"Authorization": f"Bearer {token}"}
        response = client.post("/v1/logout", headers=headers)
        assert response.status_code == 200
        json_response = response.json()
        assert "message" in json_response
        assert json_response["message"] == "User logged out successfully."

    def test_limited_endpoint(self, client):
        """
        Test the /limited endpoint for rate limiting.
        """
        for i in range(10):
            response = client.get(f"/v1/limited?user_id=testuser")
            assert response.status_code == 200
            assert response.json() == {"message": "You are within the rate limit."}

        response = client.get(f"/v1/limited?user_id=testuser")
        assert response.status_code == 429
        assert response.json()["detail"] == "Rate limit exceeded"
