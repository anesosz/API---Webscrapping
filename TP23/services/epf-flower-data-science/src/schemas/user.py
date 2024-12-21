from pydantic import BaseModel, EmailStr

class User(BaseModel):
    email: EmailStr
    password: str
    name: str
    role: str = "user"  # "user" ou "admin"
