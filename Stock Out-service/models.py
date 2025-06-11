from sqlalchemy import Column, Integer, String, Date, ForeignKey
from sqlalchemy.orm import relationship
from database import Base

class StockOut(Base):
    __tablename__ = 'stock_out'

    id = Column(Integer, primary_key=True)
    product_id = Column(Integer, nullable=False)  # masih relasi manual (tanpa foreign key antar service)
    quantity_used = Column(Integer, nullable=False)
    usage_date = Column(Date, nullable=False)
    issued_to_service = Column(String(50))
    related_id = Column(String(50))
