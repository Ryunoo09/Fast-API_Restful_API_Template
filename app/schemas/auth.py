from pydantic import BaseModel, EmailStr, ConfigDict
from typing import Optional


# ============================================================
# Request Schemas (Input)
# ============================================================

class RegisterRequest(BaseModel):
    """Schema for user registration."""
    name: str
    email: EmailStr
    password: str
    role: Optional[str] = "user"


class ResetPasswordRequest(BaseModel):
    """Schema for resetting password (authenticated user)."""
    current_password: str
    new_password: str


class RefreshTokenRequest(BaseModel):
    """Schema for refresh token request (Chapter 7 concept: refreshToken)."""
    refresh_token: str


# ============================================================
# Response Schemas (Output)
# ============================================================

class TokenResponse(BaseModel):
    """Schema for token response after login (includes refresh_token)."""
    message: str = "token_generated"
    data: dict


class RefreshTokenResponse(BaseModel):
    """Schema for token refresh response (Chapter 7 concept: token_refreshed)."""
    message: str = "token_refreshed"
    data: dict


class RegisterResponse(BaseModel):
    """Schema for registration response."""
    id: int
    name: str
    email: str
    role: str
    message: str = "User registered successfully"

    model_config = ConfigDict(from_attributes=True)


class MessageResponse(BaseModel):
    """Generic message response (matches Chapter 7 pattern)."""
    message: str
