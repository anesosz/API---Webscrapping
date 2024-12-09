from google.cloud import firestore
from fastapi import APIRouter

router = APIRouter()

# Initialize Firestore client
db = firestore.Client()

@router.post("/firestore/create")
def create_parameters():
    """
    Create Firestore collection 'parameters' with default values.
    """
    doc_ref = db.collection("parameters").document("parameters")
    doc_ref.set({
        "n_estimators": 100,
        "criterion": "gini"
    })
    return {"message": "Firestore collection 'parameters' created successfully."}

@router.get("/firestore/retrieve")
def retrieve_parameters():
    """
    Retrieve Firestore parameters.
    """
    doc_ref = db.collection("parameters").document("parameters")
    doc = doc_ref.get()
    if doc.exists:
        return doc.to_dict()
    else:
        return {"error": "Document not found."}

@router.put("/firestore/update")
def update_parameters(params: dict):
    """
    Update Firestore parameters.
    """
    doc_ref = db.collection("parameters").document("parameters")
    doc_ref.update(params)
    return {"message": "Parameters updated successfully."}
