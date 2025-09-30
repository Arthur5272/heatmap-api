from sqlalchemy import Column, Integer, String, Float, Date
from app.core.database.base import Base

class DengueIncidence(Base):
    __tablename__ = 'dengue_incidence'

    id = Column(Integer, primary_key=True, index=True)
    city = Column(String, index=True, nullable=False)
    state = Column(String, index=True, nullable=False)
    cases = Column(Integer, nullable=False)
    incidence_rate = Column(Float, nullable=False)
    date = Column(Date, nullable=False)
