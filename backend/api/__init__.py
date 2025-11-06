"""API package"""
from .auth import router as auth_router
from .upload import router as upload_router
from .match import router as match_router
from .search import router as search_router

__all__ = [
    "auth_router",
    "upload_router",
    "match_router",
    "search_router"
]
