from datetime import timedelta
from typing import Any, Optional

from fastapi import APIRouter, Depends, HTTPException, Request, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from app.core.config import settings
from app.core.database import get_db
from app.core.rate_limit import limiter
from app.core.security import (
    create_access_token,
    create_refresh_token,
    get_password_hash,
    verify_password,
)
from app.core.token_blacklist import blacklist_token, is_token_blacklisted
from app.api.dependencies import get_current_user, get_optional_current_user, oauth2_scheme
from app.models.user import User
from app.repositories.user_repository import UserRepository
from app.schemas.auth import (
    RefreshTokenRequest,
    RefreshTokenResponse,
    RegisterRequest,
    ResetPasswordRequest,
    TokenResponse,
    RegisterResponse,
    MessageResponse,
)
from app.utils.response import success_response, error_response

router = APIRouter()


# =========================================================================
# POST /register — Register a new user
# =========================================================================
@router.post("/register", response_model=RegisterResponse, status_code=status.HTTP_201_CREATED)
@limiter.limit("20/minute")
def register(
    request: Request,
    user_data: RegisterRequest,
    db: Session = Depends(get_db),
    current_user: Optional[User] = Depends(get_optional_current_user),
) -> Any:
    """
    Register a new user account.
    Rules:
    - If NOT logged in → allowed (public registration).
    - If logged in as ADMIN → allowed (admin can create users).
    - If logged in as regular USER → blocked (403 Forbidden).
    """
    # Block non-admin logged-in users from registering
    if current_user is not None and current_user.role != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You are already logged in. Only admins can register new users while authenticated.",
        )

    repo = UserRepository(db)

    # Check if email already exists
    existing_user = repo.get_by_email(user_data.email)
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered",
        )

    # Create user with hashed password
    new_user = User(
        name=user_data.name,
        email=user_data.email,
        password=get_password_hash(user_data.password),
        role=user_data.role if user_data.role else "user",
    )
    created_user = repo.create(new_user)

    return RegisterResponse(
        id=created_user.id,
        name=created_user.name,
        email=created_user.email,
        role=created_user.role,
        message="User registered successfully",
    )


# =========================================================================
# POST /login — Login and get access + refresh token
# Chapter 7 equivalent: AuthController@login → onAuthorized($token)
# =========================================================================
@router.post("/login", response_model=TokenResponse)
@limiter.limit("20/minute")
def login_access_token(
    request: Request,
    db: Session = Depends(get_db),
    form_data: OAuth2PasswordRequestForm = Depends(),
) -> Any:
    """
    OAuth2 compatible token login.
    Returns both access_token and refresh_token (Chapter 7 pattern).
    """
    user = db.query(User).filter(User.email == form_data.username).first()
    if not user or not verify_password(form_data.password, user.password):
        # Chapter 7 pattern: onUnauthorized() → { "message": "invalid_credentials" }
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="invalid_credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )

    access_token = create_access_token(
        data={"sub": str(user.id)},
        expires_delta=timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES),
    )
    refresh_token = create_refresh_token(
        data={"sub": str(user.id)},
        expires_delta=timedelta(minutes=settings.REFRESH_TOKEN_EXPIRE_MINUTES),
    )

    # Chapter 7 pattern: onAuthorized() → { "message": "token_generated", "data": { "token": ... } }
    return TokenResponse(
        message="token_generated",
        data={
            "access_token": access_token,
            "refresh_token": refresh_token,
            "token_type": "bearer",
        },
    )


# =========================================================================
# POST /refresh — Refresh access token using refresh token
# Chapter 7 equivalent: AuthController@refreshToken
# =========================================================================
@router.post("/refresh", response_model=RefreshTokenResponse)
@limiter.limit("30/minute")
def refresh_access_token(
    request: Request,
    body: RefreshTokenRequest,
    db: Session = Depends(get_db),
) -> Any:
    """
    Generate a new access token using a valid refresh token.
    Chapter 7 equivalent: refreshToken() → { "message": "token_refreshed", "data": { "token": ... } }
    """
    from jose import JWTError, jwt

    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="invalid_refresh_token",
        headers={"WWW-Authenticate": "Bearer"},
    )

    # Check if the refresh token has been blacklisted
    if is_token_blacklisted(body.refresh_token):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token has been revoked",
        )

    try:
        payload = jwt.decode(
            body.refresh_token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM]
        )
        # Ensure this is actually a refresh token, not an access token
        if payload.get("type") != "refresh":
            raise credentials_exception
        user_id: str = payload.get("sub")
        if user_id is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception

    user = db.query(User).filter(User.id == int(user_id)).first()
    if user is None:
        raise credentials_exception

    # Issue a new access token
    new_access_token = create_access_token(
        data={"sub": str(user.id)},
        expires_delta=timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES),
    )

    # Chapter 7 pattern: { "message": "token_refreshed", "data": { "token": ... } }
    return RefreshTokenResponse(
        message="token_refreshed",
        data={"access_token": new_access_token, "token_type": "bearer"},
    )


# =========================================================================
# DELETE /logout — Invalidate current token
# Chapter 7 equivalent: AuthController@invalidateToken
# =========================================================================
@router.delete("/logout", response_model=MessageResponse)
def logout(
    token: str = Depends(oauth2_scheme),
    current_user: User = Depends(get_current_user),
) -> Any:
    """
    Logout the current user by blacklisting the access token.
    Chapter 7 equivalent: invalidateToken() → { "message": "token_invalidated" }
    """
    blacklist_token(token)
    # Chapter 7 pattern: { "message": "token_invalidated" }
    return MessageResponse(message="token_invalidated")


# =========================================================================
# POST /reset-password — Change password (authenticated)
# =========================================================================
@router.post("/reset-password", response_model=MessageResponse)
def reset_password(
    password_data: ResetPasswordRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> Any:
    """
    Reset (change) the password for the currently authenticated user.
    - Requires the current password for verification.
    - Hashes and stores the new password.
    """
    # Verify current password
    if not verify_password(password_data.current_password, current_user.password):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Current password is incorrect",
        )

    # Validate new password is different
    if password_data.current_password == password_data.new_password:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="New password must be different from current password",
        )

    # Update password
    current_user.password = get_password_hash(password_data.new_password)
    db.commit()

    return MessageResponse(message="Password updated successfully")
