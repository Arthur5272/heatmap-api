from sqlalchemy import func
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.domain.models.dengue_incidence import DengueIncidence
from app.domain.schemas.dengue_incidence import DengueIncidenceCreate

class DengueRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create_incidence(self, incidence_data: DengueIncidenceCreate) -> DengueIncidence:
        new_incidence = DengueIncidence(**incidence_data.model_dump())
        self.session.add(new_incidence)
        await self.session.commit()
        await self.session.refresh(new_incidence)
        return new_incidence

    async def get_all_incidences(self) -> list[DengueIncidence]:
        result = await self.session.execute(select(DengueIncidence).order_by(DengueIncidence.date.desc()))
        return result.scalars().all()

    async def get_aggregated_cases(self, year: int, state: str | None = None) -> list[dict]:
        """
        Busca casos de dengue agregados por município, filtrando por ano e, opcionalmente, por estado.
        """
        query = (
            select(
                DengueIncidence.municipality_id,
                DengueIncidence.municipality_name,
                func.sum(DengueIncidence.cases).label("total_cases"),
            )
            .where(DengueIncidence.year == year)
            .group_by(
                DengueIncidence.municipality_id,
                DengueIncidence.municipality_name,
            )
            .order_by(DengueIncidence.municipality_name)
        )

        if state:
            query = query.where(DengueIncidence.state == state)

        result = await self.session.execute(query)
        return result.mappings().all()
