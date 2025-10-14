import folium
import pandas as pd
import branca.colormap as cm
from app.core.env.settings import settings
import requests
import json

class GenerateDengueMapUsecase:
    def __init__(self):
        pass

    async def execute(self, state: str = "PE", year: int = 2024, palette: str = "YlOrRd") -> str:
        """
        Gera um mapa HTML coroplético com dados de incidência de dengue.
        """
        print("Iniciando a geração do mapa de dengue...")

        # 1. Obter GeoJSON dos municípios do Brasil
        try:
            geojson_response = requests.get(settings.GEOJSON_SOURCE)
            geojson_response.raise_for_status()
            geojson_data = geojson_response.json()
        except requests.RequestException as e:
            print(f"Erro ao baixar GeoJSON: {e}")
            return "<h1>Erro ao carregar dados geográficos.</h1>"

        # Filtrar GeoJSON para o estado de Pernambuco (código IBGE de PE é 26)
        pe_geojson = {
            "type": "FeatureCollection",
            "features": [
                feature for feature in geojson_data["features"]
                if feature["properties"]["GEOCODIGO"].startswith("26")
            ]
        }

        # 2. Dados de dengue (simulados por enquanto)
        # Em uma implementação real, viria do DengueRepository
        mock_cases_data = {
            "2611606": 1500,  # Recife
            "2607901": 800,   # Jaboatão dos Guararapes
            "2609600": 600,   # Olinda
            "2604106": 1200,  # Caruaru
            "2610707": 950,   # Petrolina
            "2611101": 400,   # Paulista
            "2602902": 300,   # Cabo de Santo Agostinho
            # Adicionar mais municípios de PE conforme necessário
        }
        cases_map = {int(k): v for k, v in mock_cases_data.items()}
        max_cases = max(cases_map.values()) if cases_map else 1

        # 3. Criar o mapa com Folium
        map_center = [-8.34, -37.81]  # Centro de Pernambuco
        m = folium.Map(location=map_center, zoom_start=7, tiles="cartodbpositron")

        colormap = cm.LinearColormap(
            colors=['#ffffcc', '#a1dab4', '#41b6c4', '#2c7fb8', '#253494'],
            vmin=0,
            vmax=max_cases
        )
        colormap.caption = "Casos de dengue"

        def style_function(feature):
            municipality_id = int(feature['properties']['GEOCODIGO'])
            cases = cases_map.get(municipality_id, 0)
            return {
                'fillColor': colormap(cases),
                'color': 'black',
                'weight': 0.5,
                'fillOpacity': 0.7,
            }

        folium.GeoJson(
            pe_geojson,
            style_function=style_function,
            name="Municípios de Pernambuco"
        ).add_to(m)

        colormap.add_to(m)
        folium.LayerControl().add_to(m)

        print("Mapa gerado com sucesso.")
        return m._repr_html_()
