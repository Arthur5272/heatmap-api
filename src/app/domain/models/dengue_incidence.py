from sqlalchemy import Column, Integer, String, Date, DateTime, func, BigInteger
from app.core.database.base import Base

class DengueIncidence(Base):
    __tablename__ = 'dengue_cases'

    id = Column(BigInteger, primary_key=True, index=True)
    municipality_id = Column(Integer, nullable=False, index=True)
    municipality_name = Column(String, nullable=False)
    state = Column(String(2), nullable=False, index=True)
    date_report = Column(Date, nullable=False)
    cases = Column(Integer, nullable=False)
    year = Column(Integer, nullable=False, index=True)
    month = Column(Integer, nullable=False)
    source = Column(String, default='pySUS/SINAN')
    created_at = Column(DateTime, server_default=func.now(), nullable=False)
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now(), nullable=False)
