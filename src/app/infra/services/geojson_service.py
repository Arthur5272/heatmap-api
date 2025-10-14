import requests
from app.core.env.settings import settings
from functools import lru_cache

@lru_cache(maxsize=4)
def get_geojson_data(state: str = "PE"):
    """
    Busca e armazena em cache os dados GeoJSON dos municípios de um estado.
    O código IBGE dos estados é usado para filtrar os municípios.
    """
    # Mapeamento simples de sigla para código IBGE (pode ser expandido)
    state_codes = {
        "PE": "26"
        # Adicionar outros estados aqui
    }
    
    state_code = state_codes.get(state.upper())
    if not state_code:
        raise ValueError(f"Estado '{state}' não suportado.")

    try:
        geojson_response = requests.get(settings.GEOJSON_SOURCE)
        geojson_response.raise_for_status()
        geojson_data = geojson_response.json()

        # Filtrar features pelo código do estado
        state_geojson = {
            "type": "FeatureCollection",
            "features": [
                feature for feature in geojson_data["features"]
                if feature["properties"]["GEOCODIGO"].startswith(state_code)
            ]
        }
        return state_geojson

    except requests.RequestException as e:
        print(f"Erro ao baixar GeoJSON: {e}")
        return None
