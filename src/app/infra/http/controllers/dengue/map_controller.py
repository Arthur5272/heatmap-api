from fastapi import APIRouter, Depends, Query
from fastapi.responses import HTMLResponse
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database.session import get_session
from app.domain.usecases.map.generate_map_usecase import GenerateDengueMapUsecase

map_router = APIRouter()

@map_router.get("/map", response_class=HTMLResponse)
async def get_dengue_map(
    state: str = Query("PE", description="State initials (e.g., PE)"),
    year: int = Query(2024, description="Year of the data"),
    palette: str = Query("YlOrRd", description="Color palette for the map"),
    session: AsyncSession = Depends(get_session)
):
    """
    Endpoint to generate and return an interactive dengue incidence map.
    """
    usecase = GenerateDengueMapUsecase()
    map_html = await usecase.execute(state=state, year=year, palette=palette)
    return HTMLResponse(content=map_html)
