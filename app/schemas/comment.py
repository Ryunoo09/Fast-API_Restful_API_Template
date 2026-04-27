from pydantic import BaseModel
from typing import Optional


# ============================================================
# Request Schemas (Input)
# ============================================================

class CommentCreate(BaseModel):
    """Schema for creating a new comment."""
    comment: str
    post_id: int
    user_id: int


class CommentUpdate(BaseModel):
    """Schema for updating an existing comment."""
    comment: Optional[str] = None
    post_id: Optional[int] = None
    user_id: Optional[int] = None


# ============================================================
# Response Schemas (Output)
# ============================================================

class CommentResponse(BaseModel):
    """Schema for comment response."""
    id: int
    comment: str
    post_id: int
    user_id: int

    class Config:
        from_attributes = True


class CommentDeleteResponse(BaseModel):
    """Schema for comment deletion response."""
    id: int
    deleted: str


class CommentListResponse(BaseModel):
    """Schema for comment list response."""
    total: int
    comments: list[CommentResponse]
