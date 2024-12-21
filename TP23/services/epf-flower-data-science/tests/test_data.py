import pytest
from fastapi.testclient import TestClient


class TestDataRoutes:
    @pytest.fixture
    def client(self) -> TestClient:
        """
        Test client for integration tests
        """
        from main import get_application

        app = get_application()
        client = TestClient(app, base_url="http://testserver")
        return client

    def test_download_dataset(self, client):
        """
        Test the /data/download endpoint.
        """
        response = client.get("/v1/data/download")
        assert response.status_code == 200
        assert "message" in response.json() or "error" in response.json()

    def test_load_dataset(self, client):
        """
        Test the /data/load endpoint.
        """
        response = client.get("/v1/data/load")
        if response.status_code == 200:
            assert isinstance(response.json(), list)
        else:
            assert response.status_code == 200
            assert "error" in response.json()

    def test_preprocess_dataset(self, client):
        """
        Test the /data/preprocess endpoint.
        """
        response = client.get("/v1/data/preprocess")
        assert response.status_code == 200
        json_response = response.json()
        assert "message" in json_response or "error" in json_response

    def test_split_dataset(self, client):
        """
        Test the /data/split endpoint.
        """
        response = client.get("/v1/data/split")
        assert response.status_code == 200
        json_response = response.json()
        assert "message" in json_response or "error" in json_response

    def test_train_model(self, client):
        """
        Test the /model/train endpoint.
        """
        response = client.post("/v1/model/train")
        assert response.status_code == 200
        json_response = response.json()
        assert "message" in json_response or "error" in json_response

    def test_predict(self, client):
        """
        Test the /model/predict endpoint.
        """
        mock_data = [
            {"SepalLengthCm": 5.1, "SepalWidthCm": 3.5, "PetalLengthCm": 1.4, "PetalWidthCm": 0.2},
            {"SepalLengthCm": 6.5, "SepalWidthCm": 3.0, "PetalLengthCm": 5.5, "PetalWidthCm": 1.8},
        ]
        response = client.post("/v1/model/predict", json=mock_data)
        assert response.status_code == 200
        json_response = response.json()
        if response.status_code == 200:
            assert "predictions" in json_response
            assert isinstance(json_response["predictions"], list)
        else:
            assert "error" in json_response
