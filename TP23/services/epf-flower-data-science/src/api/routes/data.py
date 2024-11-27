import pandas as pd
import os
from fastapi import APIRouter
from kaggle.api.kaggle_api_extended import KaggleApi
from sklearn.model_selection import train_test_split


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
