from fastapi import APIRouter

from src.api.api_v1.endpoints import router_records, router_users

api_router = APIRouter()

api_router.include_router(router_records, prefix="/records", tags=["records"])
api_router.include_router(router_users, prefix="/users", tags=["users"])
