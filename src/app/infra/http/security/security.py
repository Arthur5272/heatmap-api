from fastapi import Security, HTTPException, status
from fastapi.security import APIKeyHeader
from app.core.env.settings import settings

api_key_header = APIKeyHeader(name="X-API-KEY")

async def get_api_key(api_key: str = Security(api_key_header)):
    if api_key == settings.SECRET_API_KEY:
        return api_key
    else:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or missing API Key",
        )
