import pytest
from sqlalchemy.ext.asyncio import AsyncSession
from app.domain.usecases.cases.get_cases_usecase import GetAggregatedCasesUsecase
from app.domain.models.dengue_incidence import DengueIncidence

@pytest.mark.asyncio
async def test_get_aggregated_cases_usecase(async_session: AsyncSession):
    # Arrange: Adicionar dados de teste ao banco de dados em memória
    test_data = [
        DengueIncidence(municipality_id=2611606, municipality_name="Recife", state="PE", date_report="2024-01-10", cases=10, year=2024, month=1),
        DengueIncidence(municipality_id=2611606, municipality_name="Recife", state="PE", date_report="2024-01-12", cases=5, year=2024, month=1),
        DengueIncidence(municipality_id=2607901, municipality_name="Jaboatão", state="PE", date_report="2024-01-15", cases=8, year=2024, month=1),
        DengueIncidence(municipality_id=2609600, municipality_name="Olinda", state="PE", date_report="2023-12-05", cases=12, year=2023, month=12),
    ]
    async_session.add_all(test_data)
    await async_session.commit()

    usecase = GetAggregatedCasesUsecase(async_session)

    # Act: Executar o caso de uso para o ano de 2024 e estado PE
    result = await usecase.execute(year=2024, state="PE")

    # Assert: Verificar se os dados agregados estão corretos
    assert len(result) == 2
    
    recife_data = next((item for item in result if item["municipality_name"] == "Recife"), None)
    jaboatao_data = next((item for item in result if item["municipality_name"] == "Jaboatão"), None)

    assert recife_data is not None
    assert jaboatao_data is not None

    assert recife_data["total_cases"] == 15
    assert jaboatao_data["total_cases"] == 8
