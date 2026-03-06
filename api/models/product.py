from sqlalchemy import Column, Integer, String, Numeric, DateTime
from sqlalchemy.sql import func
from database import Base

class Product(Base):
    __tablename__ = "products"
    
    # Definir los campos del modelo Product
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    description = Column(String, nullable=True)
    price = Column(Numeric(precision=10, scale=2))
    stock = Column(Integer, default=0)
    image_url = Column(String, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relationships
    cart_items = relationship("CartItem", back_populates="product")
    
    def __repr__(self):
        # Implementar representación del objeto
        return f"<Product id={self.id} name='{self.name}'>"