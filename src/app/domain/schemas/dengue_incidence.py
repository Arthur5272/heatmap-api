from pydantic import BaseModel, Field
from datetime import date

class DengueIncidenceSchema(BaseModel):
    id: int = Field(..., description="ID do registro")
    city: str = Field(..., description="Nome da cidade")
    state: str = Field(..., description="UF do estado")
    cases: int = Field(..., description="Número de casos confirmados")
    incidence_rate: float = Field(..., description="Taxa de incidência")
    date: date = Field(..., description="Data da ocorrência")

    class Config:
        from_attributes = True

class DengueIncidenceCreate(BaseModel):
    city: str
    state: str
    cases: int
    incidence_rate: float
    date: date
