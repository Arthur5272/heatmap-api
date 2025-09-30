from fastapi import APIRouter, Depends
from fastapi.responses import HTMLResponse
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database.session import get_session
from app.domain.usecases.map.generate_map_usecase import GenerateDengueMapUsecase

map_router = APIRouter()

@map_router.get("/map", response_class=HTMLResponse)
async def get_dengue_map(session: AsyncSession = Depends(get_session)):
    """
    Endpoint para gerar e retornar um mapa interativo da incidência de dengue.
    """
    usecase = GenerateDengueMapUsecase(session)
    map_html = await usecase.execute()
    return HTMLResponse(content=map_html)
