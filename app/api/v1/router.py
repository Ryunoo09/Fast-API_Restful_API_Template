from fastapi import APIRouter

from app.api.v1.endpoints import users, posts, comments, auth

api_router = APIRouter()

# Register all endpoint routers
api_router.include_router(auth.router, prefix="/auth", tags=["Auth"])
api_router.include_router(users.router, prefix="/users", tags=["Users"])
api_router.include_router(posts.router, prefix="/posts", tags=["Posts"])
api_router.include_router(comments.router, prefix="/comments", tags=["Comments"])
