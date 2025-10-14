from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    DATABASE_URL: str = "postgresql+asyncpg://postgres:postgres@postgres_db:5432/dengue_db"
    SYNC_DATABASE_URL: str = "postgresql+psycopg2://postgres:postgres@localhost:5432/dengue_db"
    PYTHON_ENV: str = "development"
    SCHEDULER_INTERVAL_HOURS: int = 6
    PY_SUS_YEARS: str = "2023,2024"
    GEOJSON_SOURCE: str = "https://raw.githubusercontent.com/tbrugz/geodata-br/master/geojson/geo1_br_municipios.json"
    SECRET_API_KEY: str = "your_secret_api_key"


settings = Settings()