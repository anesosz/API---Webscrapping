import pandas as pd
import os
from fastapi import APIRouter
from kaggle.api.kaggle_api_extended import KaggleApi


router = APIRouter()

# Step 6: Access the dataset
@router.get("/data/download")
def download_dataset():
    """
    Downloads the Iris dataset from Kaggle and saves it to src/data.

    Returns:
        dict: A message indicating success or error.
    """
    api = KaggleApi()
    api.authenticate()

    dataset = "uciml/iris"
    local_path = "src/data"

    os.makedirs(local_path, exist_ok=True)

    try:
        api.dataset_download_files(dataset, path=local_path, unzip=True)
        return {"message": f"Dataset downloaded successfully to {local_path}"}
    except Exception as e:
        return {"error": str(e)}

#Step 7: Loading the Iris Flower dataset
@router.get("/data/load")
def load_dataset():
    """
    Loads the Iris dataset as a JSON response.

    Returns:
        list: The dataset rows as a list of dictionaries.
    """
    file_path = "src/data/iris.csv"
    if not os.path.exists(file_path):
        return {"error": "Dataset not found. Please download it first."}
    
    try:
        df = pd.read_csv(file_path)
        return df.to_dict(orient="records")
    except Exception as e:
        return {"error": str(e)}
