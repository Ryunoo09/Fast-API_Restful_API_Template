from typing import List, Optional

from sqlalchemy.orm import Session

from app.models.comment import Comment


class CommentRepository:
    """
    Repository for Comment model.
    Handles all database operations related to comments.
    This layer is responsible ONLY for data access — no business logic here.
    """

    def __init__(self, db: Session):
        self.db = db

    def get_by_id(self, comment_id: int) -> Optional[Comment]:
        """Get a single comment by ID."""
        return self.db.query(Comment).filter(Comment.id == comment_id).first()

    def get_all(self, skip: int = 0, limit: int = 100) -> List[Comment]:
        """Get all comments with pagination."""
        return self.db.query(Comment).offset(skip).limit(limit).all()

    def get_by_post(self, post_id: int, skip: int = 0, limit: int = 100) -> List[Comment]:
        """Get all comments for a specific post."""
        return (
            self.db.query(Comment)
            .filter(Comment.post_id == post_id)
            .offset(skip)
            .limit(limit)
            .all()
        )

    def get_by_user(self, user_id: int, skip: int = 0, limit: int = 100) -> List[Comment]:
        """Get all comments by a specific user."""
        return (
            self.db.query(Comment)
            .filter(Comment.user_id == user_id)
            .offset(skip)
            .limit(limit)
            .all()
        )

    def count(self) -> int:
        """Count total comments."""
        return self.db.query(Comment).count()

    def count_by_post(self, post_id: int) -> int:
        """Count comments for a specific post."""
        return self.db.query(Comment).filter(Comment.post_id == post_id).count()

    def create(self, comment: Comment) -> Comment:
        """Create a new comment."""
        self.db.add(comment)
        self.db.commit()
        self.db.refresh(comment)
        return comment

    def update(self, comment: Comment) -> Comment:
        """Update an existing comment."""
        self.db.commit()
        self.db.refresh(comment)
        return comment

    def delete(self, comment: Comment) -> None:
        """Delete a comment."""
        self.db.delete(comment)
        self.db.commit()
