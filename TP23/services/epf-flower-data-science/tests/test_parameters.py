import pytest
from fastapi.testclient import TestClient


class TestFirestoreParameters:
    @pytest.fixture
    def client(self) -> TestClient:
        """
        Test client for integration tests
        """
        from main import get_application

        app = get_application()
        client = TestClient(app, base_url="http://testserver")
        return client

    def test_create_parameters(self, client):
        """
        Test the /firestore/create endpoint.
        """
        response = client.post("/v1/firestore/create")
        assert response.status_code == 200
        json_response = response.json()
        assert "message" in json_response
        assert json_response["message"] == "Parameters document created successfully."

    def test_retrieve_parameters(self, client):
        """
        Test the /firestore/retrieve endpoint.
        """
        response = client.get("/v1/firestore/retrieve")
        if response.status_code == 200:
            json_response = response.json()
            assert isinstance(json_response, dict)
        elif response.status_code == 404:
            json_response = response.json()
            assert "detail" in json_response
        else:
            assert response.status_code == 200  # Allowable if 500 or other errors

    def test_update_parameters(self, client):
        """
        Test the /firestore/update endpoint.
        """
        mock_params = {"n_estimators": 150, "criterion": "entropy"}
        response = client.put("/v1/firestore/update", json=mock_params)
        assert response.status_code == 200
        json_response = response.json()
        assert "message" in json_response
        assert json_response["message"] == "Parameters updated successfully."
