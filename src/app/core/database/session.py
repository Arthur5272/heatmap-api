import logging
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import OperationalError
from app.core.env.settings import settings
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from contextlib import asynccontextmanager

from app.core.database.base import Base

logger = logging.getLogger(__name__)

engine = create_engine(settings.DATABASE_URL, pool_pre_ping=True)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

async_engine = create_async_engine(settings.DATABASE_URL, echo=True)
AsyncSessionLocal = sessionmaker(
    bind=async_engine,
    class_=AsyncSession,
    expire_on_commit=False,
    autocommit=False,
    autoflush=False,
)

@asynccontextmanager
async def get_session() -> AsyncSession:
    async with AsyncSessionLocal() as session:
        yield session

def check_db_connection():
    """
    Checks if the database connection can be established.
    Runs a simple query to confirm.
    """
    try:
        db = SessionLocal()
        db.execute(text("SELECT 1"))
        logger.info("Database connection established successfully!")
        print("Database connection established successfully!")
    except OperationalError as e:
        logger.error(f"Error connecting to database: {e}")
        print(f"Error connecting to database: {e}")
        raise
    except Exception as e:
        print(f"Error connecting to the database: {e}")
        raise
    finally:
        db.close()

async def create_tables():
    """
    Cria as tabelas no banco de dados se elas não existirem.
    """
    async with async_engine.begin() as conn:
        # await conn.run_sync(Base.metadata.drop_all) # Para testes, limpa o DB
        await conn.run_sync(Base.metadata.create_all)
    print("Tabelas verificadas/criadas com sucesso.")