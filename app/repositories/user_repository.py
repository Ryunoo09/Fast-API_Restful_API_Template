from typing import List, Optional

from sqlalchemy.orm import Session

from app.models.user import User


class UserRepository:
    """
    Repository for User model.
    Handles all database operations related to users.
    This layer is responsible ONLY for data access — no business logic here.
    """

    def __init__(self, db: Session):
        self.db = db

    def get_by_id(self, user_id: int) -> Optional[User]:
        """Get a single user by ID."""
        return self.db.query(User).filter(User.id == user_id).first()

    def get_by_email(self, email: str) -> Optional[User]:
        """Get a single user by email."""
        return self.db.query(User).filter(User.email == email).first()

    def get_all(self, skip: int = 0, limit: int = 100) -> List[User]:
        """Get all users with pagination."""
        return self.db.query(User).offset(skip).limit(limit).all()

    def count(self) -> int:
        """Count total users."""
        return self.db.query(User).count()

    def create(self, user: User) -> User:
        """Create a new user."""
        self.db.add(user)
        self.db.commit()
        self.db.refresh(user)
        return user

    def update(self, user: User) -> User:
        """Update an existing user."""
        self.db.commit()
        self.db.refresh(user)
        return user

    def delete(self, user: User) -> None:
        """Delete a user."""
        self.db.delete(user)
        self.db.commit()
