from sqlalchemy.ext.asyncio import AsyncSession
from app.infra.db.repositories.dengue_repository import DengueRepository

class GetAggregatedCasesUsecase:
    def __init__(self, session: AsyncSession):
        self.dengue_repository = DengueRepository(session)

    async def execute(self, year: int, state: str | None = None) -> list[dict]:
        """
        Executa o caso de uso para buscar dados agregados de dengue.
        """
        aggregated_data = await self.dengue_repository.get_aggregated_cases(year=year, state=state)
        return aggregated_data
