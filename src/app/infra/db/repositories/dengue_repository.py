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
