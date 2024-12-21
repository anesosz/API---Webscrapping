import pytest
from unittest.mock import MagicMock
from firestore import FirestoreClient


class TestFirestoreClient:
    @pytest.fixture
    def firestore_client(self):
        """
        Create a FirestoreClient instance with mocked Firestore operations.
        """
        client = FirestoreClient()
        client.client = MagicMock() 
        return client

    def test_get_document_found(self, firestore_client):
        """
        Test FirestoreClient.get() when the document is found.
        """
        mock_doc = MagicMock()
        mock_doc.exists = True
        mock_doc.to_dict.return_value = {"field1": "value1"}
        firestore_client.client.collection.return_value.document.return_value.get.return_value = mock_doc

        result = firestore_client.get("test_collection", "test_document")
        assert result == {"field1": "value1"}

    def test_get_document_not_found(self, firestore_client):
        """
        Test FirestoreClient.get() when the document is not found.
        """
        mock_doc = MagicMock()
        mock_doc.exists = False
        firestore_client.client.collection.return_value.document.return_value.get.return_value = mock_doc

        result = firestore_client.get("test_collection", "test_document")
        assert result is None

    def test_create_document(self, firestore_client):
        """
        Test FirestoreClient.create().
        """
        firestore_client.create("test_collection", "test_document", {"field1": "value1"})
        firestore_client.client.collection.assert_called_with("test_collection")
        firestore_client.client.collection().document.assert_called_with("test_document")
        firestore_client.client.collection().document().set.assert_called_with({"field1": "value1"})

    def test_update_document(self, firestore_client):
        """
        Test FirestoreClient.update().
        """
        firestore_client.update("test_collection", "test_document", {"field1": "new_value"})
        firestore_client.client.collection.assert_called_with("test_collection")
        firestore_client.client.collection().document.assert_called_with("test_document")
        firestore_client.client.collection().document().update.assert_called_with({"field1": "new_value"})

    def test_list_all_documents(self, firestore_client):
        """
        Test FirestoreClient.list_all_documents().
        """
        mock_docs = [MagicMock(id="doc1"), MagicMock(id="doc2")]
        firestore_client.client.collection.return_value.stream.return_value = mock_docs
        for mock_doc in mock_docs:
            mock_doc.to_dict.return_value = {"field": "value"}

        result = list(firestore_client.list_all_documents("test_collection"))
        firestore_client.client.collection.assert_called_with("test_collection")
        firestore_client.client.collection().stream.assert_called()
        assert len(result) == 2
        assert result[0].id == "doc1"
        assert result[1].id == "doc2"
