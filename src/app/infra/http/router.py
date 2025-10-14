from fastapi import APIRouter
from app.infra.http.controllers.dengue.map_controller import map_router
from app.infra.http.controllers.dengue.cases_controller import cases_router
from app.infra.http.controllers.admin.admin_controller import admin_router
from app.infra.http.controllers.dengue.geojson_controller import geojson_router

api_router = APIRouter()

api_router.include_router(map_router, tags=["Dengue Map"])
api_router.include_router(cases_router, tags=["Dengue Cases"])
api_router.include_router(admin_router, tags=["Admin"])
api_router.include_router(geojson_router, tags=["GeoJSON"])