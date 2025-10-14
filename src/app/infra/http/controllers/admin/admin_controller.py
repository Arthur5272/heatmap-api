from fastapi import APIRouter, Depends, Query, BackgroundTasks
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.database.session import get_session
from app.domain.usecases.ingest.ingest_usecase import IngestDengueDataUsecase
from app.infra.http.security.security import get_api_key
from app.core.env.settings import settings

admin_router = APIRouter()

async def run_ingestion_task(session: AsyncSession, force: bool):
    """
    Função para ser executada em background.
    """
    years_str = settings.PY_SUS_YEARS
    years = [int(year.strip()) for year in years_str.split(',')]
    state_to_fetch = "PE" # Foco em Pernambuco
    
    ingest_usecase = IngestDengueDataUsecase(session)
    for year in years:
        await ingest_usecase.execute(year=year, state=state_to_fetch)

@admin_router.post("/admin/refresh")
async def refresh_dengue_data(
    background_tasks: BackgroundTasks,
    force: bool = Query(False, description="Force data refresh even if not scheduled."),
    session: AsyncSession = Depends(get_session),
    api_key: str = Depends(get_api_key)
):
    """
    Dispara a atualização dos dados de dengue via pySUS.
    A execução é feita em background para não bloquear a resposta da API.
    """
    background_tasks.add_task(run_ingestion_task, session, force)
    return {"message": "Data refresh process started in the background."}
