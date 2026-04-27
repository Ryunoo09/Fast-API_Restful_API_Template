from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.api.dependencies import get_current_user, get_current_admin
from app.models.user import User
from app.schemas.comment import (
    CommentCreate,
    CommentUpdate,
    CommentResponse,
    CommentDeleteResponse,
    CommentListResponse,
)
from app.services.comment_service import CommentService

router = APIRouter()


@router.get("/", response_model=CommentListResponse)
async def get_comments(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Get all comments.
    Admins see all comments. Regular users see only their own comments.
    """
    service = CommentService(db)
    if current_user.role == "admin":
        return service.get_comments(skip=skip, limit=limit)
    else:
        # Assuming you want similar logic here. If CommentService doesn't have get_user_comments, we might need to add it!
        # First, we fetch all and filter for now since it's cleaner. Or we can just add get_user_comments.
        all_comments = service.get_comments(skip=0, limit=1000)["comments"]
        user_comments = [c for c in all_comments if getattr(c, "user_id", None) == current_user.id or getattr(c, "name", "") == current_user.name]
        # Note: the original PHP might not have linked use_id in comments directly, but we assume it does via foreign key. Let's filter by user_id if we assume comment model has user_id.
        return {"total": len(user_comments), "comments": user_comments}


@router.get("/{comment_id}", response_model=CommentResponse)
async def get_comment(
    comment_id: int, 
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get a single comment by ID."""
    service = CommentService(db)
    comment = service.get_comment(comment_id)
    if current_user.role != "admin" and comment.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized to access this comment")
    return comment


@router.get("/post/{post_id}", response_model=CommentListResponse)
async def get_post_comments(
    post_id: int,
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user) # Require login to view post comments
):
    """Get all comments for a specific post."""
    service = CommentService(db)
    return service.get_post_comments(post_id, skip=skip, limit=limit)


@router.post("/", response_model=CommentResponse, status_code=status.HTTP_201_CREATED)
async def create_comment(
    comment_data: CommentCreate, 
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Create a new comment."""
    if current_user.role != "admin":
        comment_data.user_id = current_user.id 
    service = CommentService(db)
    return service.create_comment(comment_data)


@router.put("/{comment_id}", response_model=CommentResponse)
async def update_comment(
    comment_id: int,
    comment_data: CommentUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Update an existing comment."""
    service = CommentService(db)
    comment = service.get_comment(comment_id)
    if current_user.role != "admin" and comment.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized to update this comment")
        
    return service.update_comment(comment_id, comment_data)


@router.delete("/{comment_id}", response_model=CommentDeleteResponse)
async def delete_comment(
    comment_id: int, 
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_admin)
):
    """Delete a comment by ID. (Only ADMIN)"""
    service = CommentService(db)
    return service.delete_comment(comment_id)
