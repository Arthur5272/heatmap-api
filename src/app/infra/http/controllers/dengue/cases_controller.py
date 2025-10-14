from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.database.session import get_session
from app.domain.usecases.cases.get_cases_usecase import GetAggregatedCasesUsecase

cases_router = APIRouter()

@cases_router.get("/cases")
async def get_aggregated_cases(
    year: int = Query(..., description="Year to filter cases by."),
    state: str | None = Query(None, description="State to filter cases by (e.g., PE)."),
    session: AsyncSession = Depends(get_session),
):
    """
    Returns aggregated dengue cases per municipality.
    """
    usecase = GetAggregatedCasesUsecase(session)
    result = await usecase.execute(year=year, state=state)
    return result
