from sqlalchemy.ext.asyncio import AsyncSession
from app.infra.services.pysus_service import PySUSService
from app.infra.db.repositories.dengue_repository import DengueRepository
from app.domain.schemas.dengue_incidence import DengueIncidenceCreate
import pandas as pd

class IngestDengueDataUsecase:
    def __init__(self, session: AsyncSession):
        self.pysus_service = PySUSService()
        self.dengue_repository = DengueRepository(session)

    async def execute(self, year: int, state: str):
        """
        Orquestra o processo de download, processamento e armazenamento de dados de dengue.
        """
        print(f"Iniciando ingestão de dados para {state} em {year}...")

        # 1. Baixar dados
        dengue_df = self.pysus_service.download_dengue_data(year, state)

        if dengue_df is None or dengue_df.empty:
            print(f"Nenhum dado de dengue encontrado para {state} em {year}.")
            return

        # 2. Processar e transformar os dados
        # O DataFrame do SINAN pode ter muitas colunas. Vamos focar nas essenciais.
        # Colunas de interesse: ID_MUNICIP, DT_NOTIFIC, NU_ANO
        # ID_MUNICIP: Código do município de notificação
        # DT_NOTIFIC: Data da notificação
        # NU_ANO: Ano da notificação

        # Renomear colunas para o nosso modelo
        dengue_df_clean = dengue_df[['ID_MUNICIP', 'DT_NOTIFIC']].copy()
        dengue_df_clean['DT_NOTIFIC'] = pd.to_datetime(dengue_df_clean['DT_NOTIFIC'], errors='coerce')
        dengue_df_clean.dropna(subset=['DT_NOTIFIC', 'ID_MUNICIP'], inplace=True)

        # Agregar casos por município e dia
        daily_cases = dengue_df_clean.groupby(['ID_MUNICIP', pd.Grouper(key='DT_NOTIFIC', freq='D')]).size().reset_index(name='cases')
        daily_cases.rename(columns={'ID_MUNICIP': 'municipality_id', 'DT_NOTIFIC': 'date_report'}, inplace=True)

        print(f"Processando {len(daily_cases)} registros agregados...")

        # 3. Salvar no banco de dados (Upsert)
        for _, row in daily_cases.iterrows():
            incidence_data = DengueIncidenceCreate(
                municipality_id=int(row['municipality_id']),
                municipality_name="Unknown",  # Precisamos de um mapeamento de ID para nome
                state=state,
                date_report=row['date_report'].date(),
                cases=row['cases'],
                year=row['date_report'].year,
                month=row['date_report'].month,
            )
            # Lógica de Upsert: Verificar se já existe e atualizar, ou criar.
            # Para simplificar, estamos apenas criando. Em um cenário real, um upsert seria melhor.
            await self.dengue_repository.create_incidence(incidence_data)

        print(f"Ingestão de dados para {state} em {year} concluída.")
