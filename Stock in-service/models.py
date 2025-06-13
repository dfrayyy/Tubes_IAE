from sqlalchemy import Column, Integer, String, Date, ForeignKey, Text, DateTime, Numeric
from sqlalchemy.orm import relationship
from database import Base

class StockIn(Base):
    __tablename__ = 'stock_in'

    id = Column(Integer, primary_key=True, autoincrement=True)
    product_id = Column(Integer, nullable=False)  # jika ingin relasi lintas service, tidak pakai ForeignKey
    quantity = Column(Integer, nullable=False)
    date = Column(Date, nullable=False)
    unit_price = Column(Numeric(10, 2), nullable=False)
