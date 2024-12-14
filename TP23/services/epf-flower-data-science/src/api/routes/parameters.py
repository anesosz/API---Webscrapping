from fastapi import APIRouter, HTTPException
from firestore import FirestoreClient

router = APIRouter()
firestore_client = FirestoreClient()

# Step 13: Create Firestore Collection
@router.post("/firestore/create")
def create_parameters():
    """Create default parameters in Firestore."""
    try:
        firestore_client.create(
            "parameters", "parameters", {"n_estimators": 100, "criterion": "gini"}
        )
        return {"message": "Parameters document created successfully."}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# Step 14: Retrieve Firestore Parameters
@router.get("/firestore/retrieve")
def retrieve_parameters():
    """Retrieve parameters document."""
    try:
        data = firestore_client.get("parameters", "parameters")
        return data
    except FileNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    

# Step 15: Update Firestore Parameters
@router.put("/firestore/update")
def update_parameters(params: dict):
    """Update parameters in Firestore."""
    try:
        firestore_client.update("parameters", "parameters", params)
        return {"message": "Parameters updated successfully."}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))