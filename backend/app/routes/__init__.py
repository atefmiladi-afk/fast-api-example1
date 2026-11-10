from fastapi import APIRouter

from app.routes.category_route import router as category_router
from app.routes.progress_route import router as progress_router
from app.routes.user_route import router as user_router

api_router = APIRouter()
api_router.include_router(user_router)
api_router.include_router(category_router)
api_router.include_router(progress_router)
