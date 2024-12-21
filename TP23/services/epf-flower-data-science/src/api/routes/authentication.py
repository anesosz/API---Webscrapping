from fastapi import APIRouter, HTTPException, Depends
from google.cloud import firestore
from passlib.context import CryptContext
from firestore import FirestoreClient
from src.schemas.user import User
from src.api.dependencies.auth import validate_token



router = APIRouter()
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
firestore_client = FirestoreClient()
invalidated_tokens = []


# Step 16: Authentication 
@router.post("/register")
def register_user(user: User):
    """
    Register a new user in the Firestore database.
    Args:
        user (User): The user object containing email, password, name, and role.
    Returns:
        dict: A success message upon successful registration.    
    """
    collection_name = "users"
    existing_user = firestore_client.get(collection_name, user.email)
    
    if existing_user:
        raise HTTPException(status_code=400, detail="User already exists.")
    
    hashed_password = pwd_context.hash(user.password)
    
    firestore_client.create(
        collection_name,
        user.email,
        {
            "email": user.email,
            "name": user.name,
            "password": hashed_password,
            "role": user.role,
        }
    )
    return {"message": "User registered successfully."}


# Step 17: User management
@router.post("/login")
def login_user(email: str, password: str):
    """
    Log in an existing user by validating their credentials.
    Args:
        email (str): The user's email address.
        password (str): The user's password.
    Returns:
        dict: An access token if login is successful.
    """
    collection_name = "users"
    user = firestore_client.get(collection_name, email)
    
    if not user:
        raise HTTPException(status_code=404, detail="User not found.")
    
    if not pwd_context.verify(password, user["password"]):
        raise HTTPException(status_code=401, detail="Invalid credentials.")
    
    token = f"token-for-{email}"
    return {"access_token": token, "token_type": "bearer"}


@router.get("/users")
def list_users(email: str = Depends(validate_token)):
    """
    List all users (admin only).

    Args:
        email (str): Extracted email address of the current user.

    Returns:
        dict: A list of all users in the Firestore database.
    """
    print(f"Email after validation: {email}")  # Debugging

    # Fetch the user from Firestore
    user = firestore_client.get("users", email)
    if not user or user.get("role") != "admin":
        raise HTTPException(status_code=403, detail="Not enough permissions. Admin role required")

    # List all users in Firestore
    users = firestore_client.list_all_documents("users")
    user_list = [{"id": doc.id, "data": doc.to_dict()} for doc in users]
    return {"users": user_list}


@router.post("/logout")
def logout_user(token: str = Depends(validate_token)):
    """
    Log out the user by invalidating their token.    
    Args:
        token (str): The token of the user.    
    Returns:
        dict: A success message.
    """
    if token in invalidated_tokens:
        raise HTTPException(status_code=400, detail="User already logged out.")
    invalidated_tokens.append(token)
    return {"message": "User logged out successfully."}
