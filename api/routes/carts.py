from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from pydantic import BaseModel
from datetime import datetime
from typing import List, Optional

from database import get_db
from models.cart import Cart, CartItem

router = APIRouter()

# Schemas de Pydantic para validación de datos
class CartItemCreate(BaseModel):
    product_id: int
    quantity: int

class CartItemUpdate(BaseModel):
    quantity: int


# Endpoint para obtener el carrito del usuario
@router.get("/")
async def get_user_cart(db: Session = Depends(get_db)):
    # Implementar obtener carrito del usuario
    cart = db.query(Cart).filter(Cart.user_id == user_id).first()

    if not cart:
        raise HTTPException(status_code=404, detail="Carrito no encontrado")
    
    items = db.query(CartItem).filter(CartItem.cart_id == cart.id).all()
    return {
        "cart_id": cart.id,
        "items": [
            {
                "product_id": item.product_id,
                "quantity": item.quantity,
                "added_at": item.added_at
            }
            for item in items
        ]
    }

# Endpoint para agregar un item al carrito
@router.post("/items")
async def add_item_to_cart(db: Session = Depends(get_db)):
    # Implementar agregar item al carrito
    cart = db.query(Cart).filter(Cart.user_id == user_id).first()

    if not cart:
        # Si el carrito no existe, crear uno nuevo
        cart = Cart(user_id=user_id)
        db.add(cart)
        db.commit()
        db.refresh(cart)

    existing_item = db.query(CartItem).filter(CartItem.cart_id == cart.id, CartItem.product_id == item.product_id).first()
    if existing_item:
        existing_item.quantity += item.quantity
    else:
        new_item = CartItem(cart_id=cart.id, product_id=item.product_id, quantity=item.quantity)
        db.add(new_item)
    db.commit()
    return {"detail": "Item agregado al carrito exitosamente"}

# Endpoint para actualizar la cantidad de un item en el carrito
@router.put("/items/{item_id}")
async def update_cart_item(item_id: int, db: Session = Depends(get_db)):
    # Implementar actualizar cantidad de item
    item = db.query(CartItem).filter(CartItem.id == item_id).first()
    if not item:
        raise HTTPException(status_code=404, detail="Item no encontrado en el carrito")

    item.quantity = item_update.quantity
    db.commit()
    return {"detail": "Cantidad del item actualizada exitosamente"}

# Endpoint para remover un item del carrito
@router.delete("/items/{item_id}")
async def remove_item_from_cart(item_id: int, db: Session = Depends(get_db)):
    # Implementar remover item del carrito
    item = db.query(CartItem).filter(CartItem.id == item_id).first()
    if not item:
        raise HTTPException(status_code=404, detail="Item no encontrado en el carrito")
    db.delete(item)
    db.commit()
    return {"detail": "Item removido del carrito exitosamente"}

@router.delete("/")
async def clear_cart(db: Session = Depends(get_db)):
    # Implementar limpiar carrito
    cart = db.query(Cart).filter(Cart.user_id == user_id).first()
    if not cart:
        raise HTTPException(status_code=404, detail="Carrito no encontrado")
    db.query(CartItem).filter(CartItem.cart_id == cart.id).delete()
    db.commit()
    return {"detail": "Carrito limpiado exitosamente"}