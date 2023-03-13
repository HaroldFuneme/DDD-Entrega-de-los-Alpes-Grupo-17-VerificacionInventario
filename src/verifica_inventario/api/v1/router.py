from fastapi import APIRouter
from .orden.router import router as orden_router

router = APIRouter()
router.include_router(orden_router, prefix="/orden", tags=["Auth"])