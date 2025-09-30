from sqlalchemy.ext.asyncio import AsyncSession
from app.infra.db.repositories.dengue_repository import DengueRepository
from app.infra.services.external_fetcher import ExternalFetcherService

class IngestDengueDataUsecase:
    def __init__(self, session: AsyncSession):
        self.session = session
        self.fetcher_service = ExternalFetcherService()
        self.dengue_repository = DengueRepository(session)

    async def execute(self):
        print("Iniciando o processo de ingestão de dados de dengue...")
        
        # 1. Buscar dados da fonte externa
        dengue_data_list = await self.fetcher_service.fetch_dengue_data()
        
        if not dengue_data_list:
            print("Nenhum dado novo de dengue encontrado.")
            return

        # 2. Persistir os dados no banco de dados
        for dengue_data in dengue_data_list:
            # Aqui poderíamos adicionar uma lógica para não duplicar dados
            # Por simplicidade, vamos apenas inserir
            await self.dengue_repository.create_incidence(dengue_data)
        
        print(f"{len(dengue_data_list)} registros de dengue foram persistidos com sucesso.")
