from sqlalchemy import Column, Numeric, Integer, String
from pydantic import BaseModel

from database import Base


class Stock(Base):
    __tablename__ = "stocks"

    id = Column(Integer, primary_key=True, index=True)
    symbol = Column(String, unique=True, index=True)
    price = Column(Numeric(10, 2))
    dividend = Column(Numeric(10, 2))
    ma50 = Column(Numeric(10, 2))
    ma200 = Column(Numeric(10, 2))


class StockRequest(BaseModel):
    symbol: str
