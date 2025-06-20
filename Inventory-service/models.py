from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, Text, Date, Numeric, func
from sqlalchemy.orm import relationship
from database import Base

def format_to_idr(amount):
    if amount is None:
        return "Rp 0"
    return f"Rp {float(amount):,.2f}"

class Supplier(Base):
    __tablename__ = 'supplier'
    
    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    contact_info = Column(Text)
    address = Column(Text)
    
    # Relationships
    products = relationship('Product', back_populates='supplier')

class Product(Base):
    __tablename__ = 'product'
    
    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    description = Column(Text)
    supplier_id = Column(Integer, ForeignKey('supplier.id'))
    quantity = Column(Integer, default=0)
    unit_price = Column(Numeric(10, 2))
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())
    
    # Relationships
    supplier = relationship('Supplier', back_populates='products')
    stock_ins = relationship('StockIn', back_populates='product')
    stock_outs = relationship('StockOut', back_populates='product')

    @property
    def price_idr(self):
        return format_to_idr(self.unit_price)

class StockIn(Base):
    __tablename__ = 'stock_in'
    
    id = Column(Integer, primary_key=True)
    product_id = Column(Integer, ForeignKey('product.id'))
    quantity = Column(Integer, nullable=False)
    date = Column(Date, nullable=False)
    unit_price = Column(Numeric(10, 2))
    
    # Relationships
    product = relationship('Product', back_populates='stock_ins')

    @property
    def price_idr(self):
        return format_to_idr(self.unit_price)

class StockOut(Base):
    __tablename__ = 'stock_out'
    
    id = Column(Integer, primary_key=True)
    product_id = Column(Integer, ForeignKey('product.id'))
    quantity_used = Column(Integer, nullable=False)
    usage_date = Column(Date, nullable=False)
    issued_to_service = Column(String(50))
    related_id = Column(String(50))
    
    # Relationships
    product = relationship('Product', back_populates='stock_outs')

class InventoryUser(Base):
    __tablename__ = 'inventory_user'
    
    id = Column(Integer, primary_key=True)
    username = Column(String(100), nullable=False, unique=True)
    password_hash = Column(Text, nullable=False)
    role = Column(String(50), nullable=False)

    def __repr__(self):
        return f'<InventoryUser {self.username}>' 