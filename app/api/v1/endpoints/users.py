from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.schemas.user import (
    UserCreate,
    UserUpdate,
    UserResponse,
    UserListResponse,
)
from app.services.user_service import UserService

router = APIRouter()


@router.get("/", response_model=UserListResponse)
async def get_users(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
):
    """Get all users with pagination."""
    service = UserService(db)
    return service.get_users(skip=skip, limit=limit)


@router.get("/{user_id}", response_model=UserResponse)
async def get_user(user_id: int, db: Session = Depends(get_db)):
    """Get a single user by ID."""
    service = UserService(db)
    return service.get_user(user_id)


@router.post("/", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def create_user(user_data: UserCreate, db: Session = Depends(get_db)):
    """Create a new user."""
    service = UserService(db)
    return service.create_user(user_data)


@router.put("/{user_id}", response_model=UserResponse)
async def update_user(
    user_id: int,
    user_data: UserUpdate,
    db: Session = Depends(get_db),
):
    """Update an existing user."""
    service = UserService(db)
    return service.update_user(user_id, user_data)


@router.delete("/{user_id}")
async def delete_user(user_id: int, db: Session = Depends(get_db)):
    """Delete a user by ID."""
    service = UserService(db)
    return service.delete_user(user_id)
