from typing import List

from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.models.comment import Comment
from app.repositories.comment_repository import CommentRepository
from app.schemas.comment import CommentCreate, CommentUpdate


class CommentService:
    """
    Service layer for Comment.
    Contains all business logic related to comments.
    Mapped from PHP Chapter 3: comments table.
    """

    def __init__(self, db: Session):
        self.repository = CommentRepository(db)

    def get_comment(self, comment_id: int) -> Comment:
        """Get a comment by ID. Raises 404 if not found."""
        comment = self.repository.get_by_id(comment_id)
        if not comment:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Comment with id {comment_id} not found",
            )
        return comment

    def get_comments(self, skip: int = 0, limit: int = 100) -> dict:
        """Get all comments with pagination."""
        comments = self.repository.get_all(skip=skip, limit=limit)
        total = self.repository.count()
        return {"total": total, "comments": comments}

    def get_post_comments(self, post_id: int, skip: int = 0, limit: int = 100) -> dict:
        """Get all comments for a specific post."""
        comments = self.repository.get_by_post(post_id, skip=skip, limit=limit)
        total = self.repository.count_by_post(post_id)
        return {"total": total, "comments": comments}

    def create_comment(self, comment_data: CommentCreate) -> Comment:
        """Create a new comment."""
        comment = Comment(
            comment=comment_data.comment,
            post_id=comment_data.post_id,
            user_id=comment_data.user_id,
        )
        return self.repository.create(comment)

    def update_comment(self, comment_id: int, comment_data: CommentUpdate) -> Comment:
        """Update an existing comment."""
        comment = self.get_comment(comment_id)

        if comment_data.comment is not None:
            comment.comment = comment_data.comment
        if comment_data.post_id is not None:
            comment.post_id = comment_data.post_id
        if comment_data.user_id is not None:
            comment.user_id = comment_data.user_id

        return self.repository.update(comment)

    def delete_comment(self, comment_id: int) -> dict:
        """Delete a comment by ID."""
        comment = self.get_comment(comment_id)
        self.repository.delete(comment)
        return {"id": comment_id, "deleted": "true"}
