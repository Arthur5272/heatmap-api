import folium
import pandas as pd
from sqlalchemy.ext.asyncio import AsyncSession
from app.infra.db.repositories.dengue_repository import DengueRepository

# Dados de geolocalização simulados para as cidades
# Em um projeto real, isso viria de um banco de dados ou API de geocodificação
mock_geo_data = {
    "São Paulo": {"lat": -23.5505, "lon": -46.6333},
    "Rio de Janeiro": {"lat": -22.9068, "lon": -43.1729},
    "Belo Horizonte": {"lat": -19.9167, "lon": -43.9345},
    "Salvador": {"lat": -12.9747, "lon": -38.4767},
    "Fortaleza": {"lat": -3.7327, "lon": -38.5267},
}

class GenerateDengueMapUsecase:
    def __init__(self, session: AsyncSession):
        self.dengue_repository = DengueRepository(session)

    async def execute(self) -> str:
        """
        Gera um mapa HTML interativo com os dados de incidência de dengue.
        """
        print("Iniciando a geração do mapa de dengue...")
        
        # 1. Buscar dados do banco
        incidences = await self.dengue_repository.get_all_incidences()
        if not incidences:
            print("Nenhum dado de incidência encontrado para gerar o mapa.")
            # Retorna um mapa centrado no Brasil se não houver dados
            m = folium.Map(location=[-14.2350, -51.9253], zoom_start=4)
            return m._repr_html_()

        # 2. Processar os dados com Pandas para agregação
        data = [
            {
                "city": i.city,
                "state": i.state,
                "cases": i.cases,
                "date": i.date,
                "lat": mock_geo_data.get(i.city, {}).get("lat"),
                "lon": mock_geo_data.get(i.city, {}).get("lon"),
            }
            for i in incidences
        ]
        df = pd.DataFrame(data)

        # Agrupar por cidade para ter o total de casos e a localização
        df_agg = df.groupby('city').agg({
            'cases': 'sum',
            'lat': 'first',
            'lon': 'first'
        }).reset_index()

        # 3. Criar o mapa com Folium
        # Centraliza o mapa na primeira cidade da lista
        map_center = [df_agg['lat'].iloc[0], df_agg['lon'].iloc[0]]
        m = folium.Map(location=map_center, zoom_start=5)

        # Adicionar marcadores para cada cidade
        for _, row in df_agg.iterrows():
            if pd.notna(row['lat']) and pd.notna(row['lon']):
                folium.CircleMarker(
                    location=[row['lat'], row['lon']],
                    radius=5, # Raio do círculo
                    popup=f"Cidade: {row['city']}<br>Total de Casos: {row['cases']}",
                    color='crimson',
                    fill=True,
                    fill_color='crimson'
                ).add_to(m)

        print("Mapa gerado com sucesso.")
        # Retorna o HTML do mapa
        return m._repr_html_()
