from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from pydantic import BaseModel
from datetime import datetime
from typing import List, Optional

from database import get_db
from models.product import Product

router = APIRouter()

# Schemas de Pydantic para validación de datos
class ProductCreate(BaseModel):
    name: str
    description: Optional[str] = None
    price: float
    stock: int
    image_url: Optional[str] = None

class ProductUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    price: Optional[float] = None
    stock: Optional[int] = None
    image_url: Optional[str] = None

class ProductResponse(BaseModel):
    id: int
    name: str
    description: Optional[str] = None
    price: float
    stock: int
    image_url: Optional[str] = None
    created_at: datetime

    class Config:
        orm_mode = True

# Endpoint para obtener lista de productos
@router.get("/")
async def get_products(db: Session = Depends(get_db)):
    # Implementar obtener lista de productos
    products = db.query(Product).all()
    return [ProductResponse.from_orm(product) for product in products]

@router.get("/{product_id}")
async def get_product(product_id: int, db: Session = Depends(get_db)):
    # Implementar obtener producto por ID
    product = db.query(Product).filter(Product.id == product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Producto no encontrado")
    return ProductResponse.from_orm(product)

@router.post("/")
async def create_product(db: Session = Depends(get_db)):
    # Implementar crear producto (admin)
    product_data = ProductCreate(
        name="Producto de ejemplo",
        description="Descripción de ejemplo",
        price=9.99,
        stock=100,
        image_url=None
    )
    new_product = Product(**product_data.dict())
    db.add(new_product)
    db.commit()
    db.refresh(new_product)
    return ProductResponse.from_orm(new_product)

@router.put("/{product_id}")
async def update_product(product_id: int, product_update: ProductUpdate, db: Session = Depends(get_db)):
    # TODO: Implementar actualizar producto
    product = db.query(Product).filter(Product.id == product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Producto no encontrado")
    
    for field, value in product_update.dict(exclude_unset=True).items():
        setattr(product, field, value)
    
    db.commit()
    db.refresh(product)
    return ProductResponse.from_orm(product)

@router.delete("/{product_id}")
async def delete_product(product_id: int, db: Session = Depends(get_db)):
    # TODO: Implementar eliminar producto
    product = db.query(Product).filter(Product.id == product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Producto no encontrado")
    
    db.delete(product)
    db.commit()
    return {"detail": "Producto eliminado exitosamente"}