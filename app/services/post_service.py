from typing import List

from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.models.post import Post
from app.repositories.post_repository import PostRepository
from app.schemas.post import PostCreate, PostUpdate


class PostService:
    """
    Service layer for Post.
    Contains all business logic related to posts.
    Mapped from PHP Chapter 3: posts.php functions.
    """

    def __init__(self, db: Session):
        self.repository = PostRepository(db)

    def get_post(self, post_id: int) -> Post:
        """
        Get a post by ID. Raises 404 if not found.
        Equivalent to PHP: getPost($db, $id)
        """
        post = self.repository.get_by_id(post_id)
        if not post:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Post with id {post_id} not found",
            )
        return post

    def get_posts(self, skip: int = 0, limit: int = 100) -> dict:
        """
        Get all posts with pagination.
        Equivalent to PHP: getAllPosts($db)
        """
        posts = self.repository.get_all(skip=skip, limit=limit)
        total = self.repository.count()
        return {"total": total, "posts": posts}

    def get_user_posts(self, user_id: int, skip: int = 0, limit: int = 100) -> List[Post]:
        """Get all posts belonging to a specific user."""
        return self.repository.get_by_user(user_id, skip=skip, limit=limit)

    def create_post(self, post_data: PostCreate) -> dict:
        """
        Create a new post.
        Equivalent to PHP: addPost($input, $db)
        Returns post data with a link field as in the PHP version.
        """
        post = Post(
            title=post_data.title,
            status=post_data.status.value,
            content=post_data.content,
            user_id=post_data.user_id,
        )
        created_post = self.repository.create(post)

        # Return with link field (same as PHP version)
        return {
            "id": created_post.id,
            "title": created_post.title,
            "status": created_post.status,
            "content": created_post.content,
            "user_id": created_post.user_id,
            "link": f"/posts/{created_post.id}",
        }

    def update_post(self, post_id: int, post_data: PostUpdate) -> Post:
        """
        Update an existing post.
        Equivalent to PHP: updatePost($input, $db, $postId)
        Only updates fields that are provided (not None).
        """
        post = self.get_post(post_id)

        # Update only provided fields (same as PHP bindAllValues with allowedFields)
        if post_data.title is not None:
            post.title = post_data.title
        if post_data.status is not None:
            post.status = post_data.status.value
        if post_data.content is not None:
            post.content = post_data.content
        if post_data.user_id is not None:
            post.user_id = post_data.user_id

        return self.repository.update(post)

    def delete_post(self, post_id: int) -> dict:
        """
        Delete a post by ID.
        Equivalent to PHP: deletePost($db, $id)
        Returns id and deleted status as in the PHP version.
        """
        post = self.get_post(post_id)
        self.repository.delete(post)
        return {"id": post_id, "deleted": "true"}
