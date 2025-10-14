from fastapi import FastAPI
from fastapi.responses import JSONResponse
from app.core.database.session import check_db_connection, create_tables
from app.infra.http.router import api_router
from app.core.scheduler import start_scheduler, stop_scheduler, run_ingestion

app = FastAPI(
    title="Dengue Heatmap API",
    version="0.1.0",
    description="API for dengue heatmap data.",
)

@app.on_event("startup")
async def startup_event():
    """
    Event that runs at application startup.
    Checks the database connection.
    """
    print("Iniciando a aplicação...")
    check_db_connection()
    await create_tables()
    
    # Executa a primeira ingestão imediatamente
    await run_ingestion()
    
    # Inicia o agendador
    start_scheduler()
    print("Aplicação iniciada com sucesso.")

@app.on_event("shutdown")
def shutdown_event():
    """
    Event that runs at application shutdown.
    Stops the scheduler.
    """
    print("Encerrando a aplicação...")
    stop_scheduler()
    print("Aplicação encerrada com sucesso.")


@app.get("/")
async def read_root():
    """
    Root endpoint that returns a welcome message.
    """
    return JSONResponse(content={"message": "API started!"})


@app.get("/health")
async def health_check():
    """
    Health check endpoint.
    """
    return JSONResponse(content={"status": "ok"})


app.include_router(api_router, prefix="/api/v1")