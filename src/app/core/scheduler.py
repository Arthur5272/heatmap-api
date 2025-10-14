from apscheduler.schedulers.asyncio import AsyncIOScheduler
from app.core.database.session import get_session
from app.domain.usecases.ingest.ingest_usecase import IngestDengueDataUsecase
from app.core.env.settings import settings

async def run_ingestion():
    """
    Função wrapper para obter uma sessão de banco de dados e
    executar o use case de ingestão para os anos configurados.
    """
    years_str = settings.PY_SUS_YEARS
    years = [int(year.strip()) for year in years_str.split(',')]
    
    # Por enquanto, vamos focar em Pernambuco (PE)
    state_to_fetch = "PE"

    print(f"Iniciando job de ingestão para os anos: {years} no estado: {state_to_fetch}")

    async with get_session() as session:
        ingest_usecase = IngestDengueDataUsecase(session)
        for year in years:
            await ingest_usecase.execute(year=year, state=state_to_fetch)
    
    print("Job de ingestão concluído.")

scheduler = AsyncIOScheduler()

def start_scheduler():
    """
    Inicia o agendador para executar a ingestão de dados periodicamente.
    """
    interval_hours = settings.SCHEDULER_INTERVAL_HOURS
    scheduler.add_job(run_ingestion, 'interval', hours=interval_hours, id='dengue_ingestion_job')
    
    if not scheduler.running:
        scheduler.start()
        print(f"Agendador iniciado. A ingestão de dados será executada a cada {interval_hours} hora(s).")
    else:
        print("Agendador já está em execução.")

def stop_scheduler():
    """
    Para o agendador se ele estiver em execução.
    """
    if scheduler.running:
        scheduler.shutdown()
        print("Agendador parado.")
