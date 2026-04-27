from typing import List, Optional

from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.core.security import get_password_hash
from app.models.user import User
from app.repositories.user_repository import UserRepository
from app.schemas.user import UserCreate, UserUpdate


class UserService:
    """
    Service layer for User.
    Contains all business logic related to users.
    Orchestrates between repositories and schemas.
    """

    def __init__(self, db: Session):
        self.repository = UserRepository(db)

    def get_user(self, user_id: int) -> User:
        """Get a user by ID. Raises 404 if not found."""
        user = self.repository.get_by_id(user_id)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"User with id {user_id} not found",
            )
        return user

    def get_users(self, skip: int = 0, limit: int = 100) -> dict:
        """Get all users with pagination."""
        users = self.repository.get_all(skip=skip, limit=limit)
        total = self.repository.count()
        return {"total": total, "users": users}

    def create_user(self, user_data: UserCreate) -> User:
        """
        Create a new user.
        Validates uniqueness of email before creation.
        Password is hashed before storing.
        """
        # Check if email already exists
        if self.repository.get_by_email(user_data.email):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email already registered",
            )

        # Create user model with hashed password
        user = User(
            name=user_data.name,
            email=user_data.email,
            password=get_password_hash(user_data.password),
        )

        return self.repository.create(user)

    def update_user(self, user_id: int, user_data: UserUpdate) -> User:
        """Update an existing user."""
        user = self.get_user(user_id)

        # Update only provided fields
        if user_data.name is not None:
            user.name = user_data.name

        if user_data.email is not None:
            # Check email uniqueness
            existing = self.repository.get_by_email(user_data.email)
            if existing and existing.id != user_id:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Email already registered",
                )
            user.email = user_data.email

        if user_data.password is not None:
            user.password = get_password_hash(user_data.password)

        return self.repository.update(user)

    def delete_user(self, user_id: int) -> dict:
        """Delete a user by ID."""
        user = self.get_user(user_id)
        self.repository.delete(user)
        return {"message": f"User with id {user_id} deleted successfully"}
