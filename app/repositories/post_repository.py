from typing import List, Optional

from sqlalchemy.orm import Session

from app.models.post import Post


class PostRepository:
    """
    Repository for Post model.
    Handles all database operations related to posts.
    This layer is responsible ONLY for data access — no business logic here.
    """

    def __init__(self, db: Session):
        self.db = db

    def get_by_id(self, post_id: int) -> Optional[Post]:
        """Get a single post by ID."""
        return self.db.query(Post).filter(Post.id == post_id).first()

    def get_all(self, skip: int = 0, limit: int = 100) -> List[Post]:
        """Get all posts with pagination."""
        return self.db.query(Post).offset(skip).limit(limit).all()

    def get_by_user(self, user_id: int, skip: int = 0, limit: int = 100) -> List[Post]:
        """Get all posts belonging to a specific user."""
        return (
            self.db.query(Post)
            .filter(Post.user_id == user_id)
            .offset(skip)
            .limit(limit)
            .all()
        )

    def count(self) -> int:
        """Count total posts."""
        return self.db.query(Post).count()

    def create(self, post: Post) -> Post:
        """Create a new post."""
        self.db.add(post)
        self.db.commit()
        self.db.refresh(post)
        return post

    def update(self, post: Post) -> Post:
        """Update an existing post."""
        self.db.commit()
        self.db.refresh(post)
        return post

    def delete(self, post: Post) -> None:
        """Delete a post."""
        self.db.delete(post)
        self.db.commit()
