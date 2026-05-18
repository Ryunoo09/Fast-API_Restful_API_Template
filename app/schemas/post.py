from pydantic import BaseModel, ConfigDict
from typing import Optional
from enum import Enum


class PostStatus(str, Enum):
    """Enum for post status matching MySQL ENUM('draft', 'published')."""
    draft = "draft"
    published = "published"


# ============================================================
# Request Schemas (Input)
# ============================================================

class PostCreate(BaseModel):
    """Schema for creating a new post."""
    title: str
    status: PostStatus = PostStatus.draft
    content: str
    user_id: int


class PostUpdate(BaseModel):
    """Schema for updating an existing post."""
    title: Optional[str] = None
    status: Optional[PostStatus] = None
    content: Optional[str] = None
    user_id: Optional[int] = None


# ============================================================
# Response Schemas (Output)
# ============================================================

class PostResponse(BaseModel):
    """Schema for post response."""
    id: int
    title: str
    status: str
    content: str
    user_id: int

    model_config = ConfigDict(from_attributes=True)


class PostCreateResponse(BaseModel):
    """Schema for post creation response (includes link)."""
    id: int
    title: str
    status: str
    content: str
    user_id: int
    link: str

    model_config = ConfigDict(from_attributes=True)


class PostDeleteResponse(BaseModel):
    """Schema for post deletion response."""
    id: int
    deleted: str


class PostListResponse(BaseModel):
    """Schema for post list response."""
    total: int
    posts: list[PostResponse]
