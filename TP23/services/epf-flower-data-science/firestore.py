import os
from google.cloud import firestore
from google.oauth2 import service_account



class FirestoreClient:
    """Wrapper around a database"""

    client: firestore.Client

    def __init__(self) -> None:
        """Init the client."""
        # Path to the service account key
        key_path = os.getenv("FIRESTORE_KEY_PATH", "src/config/firestore_key.json")
        
        # Load credentials from the JSON file
        credentials = service_account.Credentials.from_service_account_file(key_path)

        self.client = firestore.Client(credentials=credentials)

    def get(self, collection_name: str, document_id: str) -> dict:
        """Find one document by ID.
        Args:
            collection_name: The collection name
            document_id: The document id
        Return:
            Document value.
        """
        doc = self.client.collection(
            collection_name).document(document_id).get()
        if doc.exists:
            return doc.to_dict()
        raise FileExistsError(
            f"No document found at {collection_name} with the id {document_id}"
        )

    def create(self, collection_name: str, document_id: str, data: dict) -> None:
        """Create a new document."""
        self.client.collection(collection_name).document(document_id).set(data)

    def update(self, collection_name: str, document_id: str, updates: dict) -> None:
        """Update an existing document."""
        self.client.collection(collection_name).document(document_id).update(updates)