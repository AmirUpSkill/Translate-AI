from fastapi import APIRouter 
from .endpoints import translate_router 

# --- Main V1 Router --- 
v1_router = APIRouter()
# ---translate endpoints under /api/v1 --- 
v1_router.include_router(translate_router, prefix="/api/v1", tags=["translation"])