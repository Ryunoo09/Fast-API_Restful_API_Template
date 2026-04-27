from pydantic import BaseModel, EmailStr
from typing import Optional


# ============================================================
# Request Schemas (Input)
# ============================================================

class UserCreate(BaseModel):
    """Schema for creating a new user."""
    name: str
    email: EmailStr
    password: str
    role: Optional[str] = "user"


class UserUpdate(BaseModel):
    """Schema for updating an existing user."""
    name: Optional[str] = None
    email: Optional[EmailStr] = None
    password: Optional[str] = None
    role: Optional[str] = None


# ============================================================
# Response Schemas (Output)
# ============================================================

class UserResponse(BaseModel):
    """Schema for user response (excludes password)."""
    id: int
    name: str
    email: str
    role: str

    class Config:
        from_attributes = True


class UserListResponse(BaseModel):
    """Schema for user list response."""
    total: int
    users: list[UserResponse]
