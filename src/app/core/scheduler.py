from apscheduler.schedulers.asyncio import AsyncIOScheduler
from app.core.database.session import get_session
from app.domain.usecases.ingest.ingest_usecase import IngestDengueDataUsecase

async def run_ingestion():
    """
    Função wrapper para obter uma sessão de banco de dados e
    executar o use case de ingestão.
    """
    async with get_session() as session:
        ingest_usecase = IngestDengueDataUsecase(session)
        await ingest_usecase.execute()

scheduler = AsyncIOScheduler()

def start_scheduler():
    """
    Inicia o agendador para executar a ingestão de dados periodicamente.
    """
    # Adiciona o job para rodar a cada 1 minuto
    scheduler.add_job(run_ingestion, 'interval', minutes=1, id='dengue_ingestion_job')
    
    if not scheduler.running:
        scheduler.start()
        print("Agendador iniciado. A ingestão de dados será executada a cada 1 minuto.")
    else:
        print("Agendador já está em execução.")

def stop_scheduler():
    """
    Para o agendador se ele estiver em execução.
    """
    if scheduler.running:
        scheduler.shutdown()
        print("Agendador parado.")
