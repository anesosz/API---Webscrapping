import os
import json
import pandas as pd
from fastapi import APIRouter
from kaggle.api.kaggle_api_extended import KaggleApi
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
import joblib
from typing import List



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
    

# Step 8: Processing the Dataset
@router.get("/data/preprocess")
def preprocess_dataset():
    """
    Preprocess the dataset by encoding categorical variables
    and saving the processed data to src/data/iris_processed.csv.
    """
    file_path = "src/data/iris.csv"
    processed_path = "src/data/iris_processed.csv"
    
    if not os.path.exists(file_path):
        return {"error": "Dataset not found. Please download it first."}
    
    try:
        df = pd.read_csv(file_path)
        df['Species'] = df['Species'].astype('category').cat.codes
        df.to_csv(processed_path, index=False)
        return {"message": f"Dataset preprocessed and saved to {processed_path}"}
    except Exception as e:
        return {"error": str(e)}


# Step 9: Split in train and test
@router.get("/data/split")
def split_dataset():
    """
    Split the preprocessed dataset into training and testing sets.
    Save the splits to src/data/train.csv and src/data/test.csv.
    """
    processed_path = "src/data/iris_processed.csv"
    if not os.path.exists(processed_path):
        return {"error": "Processed dataset not found. Please preprocess it first."}
    
    try:
        df = pd.read_csv(processed_path)

        if 'Id' in df.columns:
            df = df.drop(columns=['Id'])
        
        X = df.drop(columns=["Species"])
        y = df["Species"]

        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

        X_train.to_csv("src/data/train.csv", index=False)
        X_test.to_csv("src/data/test.csv", index=False)
        y_train.to_csv("src/data/y_train.csv", index=False)
        y_test.to_csv("src/data/y_test.csv", index=False)
        
        return {"message": "Dataset split successfully and saved in src/data directory."}
    except Exception as e:
        return {"error": str(e)}

# Step 11: Train the Classification Model
@router.post("/model/train")
def train_model():
    """
    Train a classification model using the preprocessed dataset.
    Save the trained model to src/models.
    """
    try:
        train_path = "src/data/train.csv"
        y_train_path = "src/data/y_train.csv"
        params_path = "src/config/model_parameters.json"
        model_path = "src/models/random_forest_model.pkl"

        if not os.path.exists(train_path) or not os.path.exists(y_train_path):
            return {"error": "Training data not found. Please split the dataset first."}

        X_train = pd.read_csv(train_path)
        y_train = pd.read_csv(y_train_path).squeeze()  

        with open(params_path, "r") as f:
            params = json.load(f)

        model = RandomForestClassifier(**params)
        model.fit(X_train, y_train)

        os.makedirs("src/models", exist_ok=True)
        joblib.dump(model, model_path)

        return {"message": f"Model trained and saved at {model_path}"}
    except Exception as e:
        return {"error": str(e)}

 # Step 12: Prediction with Trained Model
@router.post("/model/predict")
def predict(data: List[dict]):
    """
    Make predictions using the trained model.
    Input: JSON data as a list of validated features.
    Output: Predictions as JSON.
    """
    try:
        model_path = "src/models/random_forest_model.pkl"
        if not os.path.exists(model_path):
            return {"error": "Trained model not found. Please train the model first."}

        model = joblib.load(model_path)

        X_input = pd.DataFrame(data)
        print("Input DataFrame:\n", X_input)

        predictions = model.predict(X_input)
        print("Predictions:", predictions)
        print("Type of predictions:", type(predictions))
        if hasattr(predictions, "dtype"):
            print("Dtype of predictions:", predictions.dtype)

        reverse_species_mapping = {0: "Iris-setosa", 1: "Iris-versicolor", 2: "Iris-virginica"}
        formatted_predictions = [
            f"{pred} ({reverse_species_mapping[pred]})" for pred in predictions
        ]
        
        return {"predictions": formatted_predictions}
    
    except Exception as e:
        return {"error": str(e)}