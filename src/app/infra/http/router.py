from fastapi import APIRouter
from app.infra.http.controllers.dengue.map_controller import map_router

api_router = APIRouter()

api_router.include_router(map_router, tags=["Dengue Map"])