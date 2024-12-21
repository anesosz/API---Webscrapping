from fastapi import HTTPException, Depends
from firestore import FirestoreClient
from datetime import datetime


firestore_client = FirestoreClient()

invalidated_tokens = []


# def validate_token(token: str):
#     """
#     Validate the Bearer Token.
#     Args:
#         token (str): The Bearer Token from the Authorization header.
#     Returns:
#         str: The email address of the authenticated user.
#     Raises:
#         HTTPException: If the token is invalid.
#     """
#     if token in invalidated_tokens:
#         raise HTTPException(status_code=401, detail="Token has been invalidated.")
#     if not token.startswith("token-for-"):
#         raise HTTPException(status_code=401, detail="Invalid token format.")
#     return token.replace("token-for-", "")

def validate_token(token: str):
    print(f"Received token in validate_token: {token}")  # Debugging
    if token in invalidated_tokens:
        raise HTTPException(status_code=401, detail="Token has been invalidated.")
    if not token.startswith("token-for-"):
        raise HTTPException(status_code=401, detail="Invalid token format.")
    email = token.replace("token-for-", "")
    print(f"Extracted email: {email}")  # Debugging
    return email


def get_current_user(token: str = Depends(validate_token)):
    """
    Extract the current user from the token.

    Args:
        token (str): The Bearer Token.

    Returns:
        str: The email of the authenticated user.
    """
    return token


def get_current_user_with_role(
    token: str = Depends(validate_token), role: str = "user"
):
    """
    Extract the current user from the token and verify their role.

    Args:
        token (str): The Bearer Token.
        role (str): The required role for the user (default is "user").

    Returns:
        dict: The user object from Firestore.

    Raises:
        HTTPException: If the user's role does not match the required role.
    """
    email = validate_token(token)
    user = firestore_client.get("users", email)

    if user["role"] != role:
        raise HTTPException(status_code=403, detail="Not enough permissions.")

    return user


def get_current_admin(token: str = Depends(validate_token)):
    """
    Verify that the current user is an admin.

    Args:
        token (str): The Bearer Token.

    Returns:
        str: The email of the authenticated admin user.

    Raises:
        HTTPException: If the user is not an admin.
    """
    email = validate_token(token)
    user = firestore_client.get("users", email)
    if user["role"] != "admin":
        raise HTTPException(status_code=403, detail="Not enough permissions.")
    return email


rate_limit_data = {}

def rate_limit(user_id: str, limit: int = 10, interval: int = 60):
    """
    Implements rate limiting using a Python dictionary.

    Args:
        user_id (str): The unique identifier of the user.
        limit (int): The maximum number of allowed requests within the interval.
        interval (int): The time window in seconds for the rate limit.

    Raises:
        HTTPException: If the user exceeds the rate limit.
    """
    now = datetime.now()
    
    if user_id in rate_limit_data:
        request_times = rate_limit_data[user_id]
        
        rate_limit_data[user_id] = [t for t in request_times if (now - t).seconds < interval]

        if len(rate_limit_data[user_id]) >= limit:
            raise HTTPException(status_code=429, detail="Rate limit exceeded")
        else:
            rate_limit_data[user_id].append(now)
    else:
        rate_limit_data[user_id] = [now]