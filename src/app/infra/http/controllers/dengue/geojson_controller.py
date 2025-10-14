from fastapi import APIRouter, Query, HTTPException, status
from app.infra.services.geojson_service import get_geojson_data

geojson_router = APIRouter()

@geojson_router.get("/geojson/municipios")
async def get_municipalities_geojson(
    state: str = Query("PE", description="State abbreviation (e.g., PE).")
):
    """
    Returns the GeoJSON of the municipalities for a given state.
    """
    try:
        geojson_data = get_geojson_data(state=state)
        if geojson_data:
            return geojson_data
        else:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"GeoJSON data not found for state '{state}'.",
            )
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e),
        )
