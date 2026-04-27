from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.api.dependencies import get_current_user, get_current_admin
from app.models.user import User
from app.schemas.post import (
    PostCreate,
    PostUpdate,
    PostResponse,
    PostCreateResponse,
    PostDeleteResponse,
    PostListResponse,
)
from app.services.post_service import PostService

router = APIRouter()


@router.get("/", response_model=PostListResponse)
async def get_posts(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Get all posts.
    Admins see all posts. Regular users see only their own posts.
    """
    service = PostService(db)
    if current_user.role == "admin":
        return service.get_posts(skip=skip, limit=limit)
    else:
        posts = service.get_user_posts(current_user.id, skip=skip, limit=limit)
        return {"total": len(posts), "posts": posts}


@router.get("/{post_id}", response_model=PostResponse)
async def get_post(
    post_id: int, 
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Get a single post by ID.
    Users can only get their own posts unless they are admin.
    """
    service = PostService(db)
    post = service.get_post(post_id)
    if current_user.role != "admin" and post.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized to access this post")
    return post


@router.post("/", response_model=PostCreateResponse, status_code=status.HTTP_201_CREATED)
async def create_post(
    post_data: PostCreate, 
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Create a new post. (Users can create posts for themselves).
    """
    # Force user_id to be current_user.id if not admin
    if current_user.role != "admin":
        post_data.user_id = current_user.id
        
    service = PostService(db)
    return service.create_post(post_data)


@router.put("/{post_id}", response_model=PostResponse)
async def update_post(
    post_id: int,
    post_data: PostUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Update an existing post.
    Users can only update their own posts.
    """
    service = PostService(db)
    post = service.get_post(post_id)
    if current_user.role != "admin" and post.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized to update this post")
    
    return service.update_post(post_id, post_data)


@router.delete("/{post_id}", response_model=PostDeleteResponse)
async def delete_post(
    post_id: int, 
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_admin)
):
    """
    Delete a post by ID. (Only ADMIN can perform DELETE)
    """
    service = PostService(db)
    return service.delete_post(post_id)
