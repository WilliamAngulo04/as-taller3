from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from pydantic import BaseModel, EmailStr
from passlib.context import CryptContext
from datetime import datetime
from typing import List, Optional

from database import get_db
from models.user import User

router = APIRouter()

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

#Schemas de Pydantic para validación de datos
class UserCreate(BaseModel):
    username: str
    email: EmailStr
    password: str

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class UserProfile(BaseModel):
    id: int
    username: str
    email: EmailStr
    is_active: bool

    class Config:
        orm_mode = True

# Funciones auxiliares
def get_password_hash(password):
    return pwd_context.hash(password)

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

# Endpoint de registro de usuario
@router.post("/register")
async def register_user(user: UserCreate, db: Session = Depends(get_db)):
    # Verificar si el usuario ya existe
    existing_user = db.query(User).filter(User.email == user.email).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="El correo electrónico ya está registrado")

    # Crear nuevo usuario
    hashed_password = get_password_hash(user.password)
    new_user = User(
        username=user.username,
        email=user.email,
        password_hash=hashed_password
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    
    return UserProfile.from_orm(new_user)

# Endpoint de login de usuario
@router.post("/login")  
async def login_user(user: UserLogin, db: Session = Depends(get_db)):
    # Implementar login de usuario
    db_user = db.query(User).filter(User.email == user.email).first()
    if not db_user or not verify_password(user.password, db_user.password_hash):
        raise HTTPException(status_code=400, detail="Correo electrónico o contraseña incorrectos")
    return UserProfile.from_orm(db_user)

# Endpoint para obtener perfil de usuario
@router.get("/profile")
async def get_user_profile(db: Session = Depends(get_db)):
    # Implementar obtener perfil de usuario
    user = db.query(User).filter(User.id == 1).first()
    if not user:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    return UserProfile.from_orm(user)

# Endpoint para actualizar perfil de usuario
@router.put("/profile")
async def update_user_profile(db: Session = Depends(get_db)):
    # Implementar actualizar perfil de usuario
    user = db.query(User).filter(User.id == 1).first()
    if not user:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    
    if user.is_active:
        user.is_active = False

    else:
        user.is_active = True
    db.commit()
    db.refresh(user)
    return UserProfile.from_orm(user)