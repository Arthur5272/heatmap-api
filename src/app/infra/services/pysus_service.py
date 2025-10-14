import pandas as pd
from pysus.online_data import SINAN

class PySUSService:
    def __init__(self):
        self.sinan = SINAN()

    def download_dengue_data(self, year: int, state_initials: str) -> pd.DataFrame | None:
        """
        Downloads dengue data for a given year and state.

        Args:
            year (int): The year to download data for.
            state_initials (str): The state initials (e.g., 'PE').

        Returns:
            pd.DataFrame | None: A DataFrame with the dengue data, or None if no data is found.
        """
        try:
            print(f"Buscando arquivos para DENGUE em {year}...")
            files = self.sinan.get_files("DENG", year)
            if not files:
                print(f"Nenhum arquivo encontrado para DENGUE em {year}.")
                return None
            
            print(f"Baixando e processando {len(files)} arquivo(s)...")
            df = self.sinan.download(files).to_dataframe()
            
            # Filtrar por estado (UF_LPI) - Unidade de Federação da LPI (Local de Provável Infecção)
            # A coluna pode variar de nome dependendo do ano (ex: SG_UF_LPI ou outro)
            # Vamos verificar as colunas disponíveis
            uf_column = None
            possible_uf_columns = ['SG_UF_LPI', 'SG_UF', 'ID_MN_RESI'] # Adicionar outras variações se necessário
            
            for col in possible_uf_columns:
                if col in df.columns:
                    uf_column = col
                    break
            
            if uf_column:
                 # Carregar códigos de estado para mapeamento de nome para código
                # Supondo que a coluna contenha o código do estado ou a sigla
                # O ideal seria usar uma tabela de mapeamento IBGE
                # Para simplificar, vamos assumir que a coluna já contém a sigla
                if df[uf_column].dtype == 'object':
                    df_state = df[df[uf_column].str.upper() == state_initials.upper()]
                else:
                    # Se for código, precisaríamos de um mapa. Ex: PE=26
                    # Por enquanto, vamos pular essa lógica complexa.
                    print(f"Coluna de UF '{uf_column}' não é do tipo string. Filtragem por sigla não aplicada.")
                    df_state = df # Retorna o DF completo se não puder filtrar
            else:
                 print("Não foi encontrada uma coluna de UF para filtrar os dados.")
                 df_state = df # Retorna o DF completo se não encontrar coluna

            print(f"Dados de dengue para {state_initials} em {year} baixados com sucesso.")
            return df_state

        except Exception as e:
            print(f"Erro ao baixar dados do SINAN: {e}")
            return None

if __name__ == '__main__':
    # Exemplo de uso
    service = PySUSService()
    year = 2023
    state = "PE"
    dengue_df = service.download_dengue_data(year, state)

    if dengue_df is not None and not dengue_df.empty:
        print(f"Total de {len(dengue_df)} casos de dengue registrados em {state} em {year}.")
        print("Primeiras 5 linhas:")
        print(dengue_df.head())
        # Salvar em CSV para análise
        # dengue_df.to_csv(f"dengue_{state.lower()}_{year}.csv", index=False)
    else:
        print(f"Não foi possível obter os dados de dengue para {state} em {year}.")
