import pandas as pd
import os
from fastapi import APIRouter
from kaggle.api.kaggle_api_extended import KaggleApi
from sklearn.ensemble import RandomForestClassifier
import joblib

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


# Step 11: Train the Model
@router.post("/model/train", tags=["Model Training"])
def train_model():
    """
    Train a classification model using the preprocessed dataset.
    Save the trained model in src/models.
    """
    try:
        # Load the preprocessed dataset
        processed_path = "src/data/iris_processed.csv"
        if not os.path.exists(processed_path):
            return {"error": "Processed dataset not found. Please preprocess it first."}
        
        df = pd.read_csv(processed_path)
        X = df.drop(columns=["species"])
        y = df["species"]

        # Load parameters
        with open("src/config/model_parameters.json", "r") as f:
            params = json.load(f)

        # Train the model
        model = RandomForestClassifier(**params)
        model.fit(X, y)

        # Save the trained model
        model_path = "src/models/random_forest_model.pkl"
        joblib.dump(model, model_path)
        return {"message": f"Model trained and saved at {model_path}"}
    except Exception as e:
        return {"error": str(e)}