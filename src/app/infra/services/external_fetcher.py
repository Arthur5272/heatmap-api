import random
from datetime import date, timedelta
from app.domain.schemas.dengue_incidence import DengueIncidenceCreate

class ExternalFetcherService:
    """
    Serviço para simular a busca de dados de incidência de dengue de uma fonte externa.
    """
    async def fetch_dengue_data(self) -> list[DengueIncidenceCreate]:
        """
        Simula a obtenção de novos dados de incidência de dengue.
        Retorna uma lista de objetos DengueIncidenceCreate com dados fictícios.
        """
        cities_states = [
            ("São Paulo", "SP"),
            ("Rio de Janeiro", "RJ"),
            ("Belo Horizonte", "MG"),
            ("Salvador", "BA"),
            ("Fortaleza", "CE"),
        ]
        
        fetched_data = []
        for city, state in cities_states:
            # Simula dados para os últimos 5 dias
            for i in range(5):
                random_date = date.today() - timedelta(days=i)
                new_data = DengueIncidenceCreate(
                    city=city,
                    state=state,
                    cases=random.randint(10, 500),
                    incidence_rate=round(random.uniform(10.0, 500.0), 2),
                    date=random_date,
                )
                fetched_data.append(new_data)
        
        print(f"Simulando busca: {len(fetched_data)} novos registros de dengue encontrados.")
        return fetched_data
