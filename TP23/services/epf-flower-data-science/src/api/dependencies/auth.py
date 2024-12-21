from fastapi import HTTPException, Depends
from firestore import FirestoreClient

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