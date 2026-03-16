from datetime import timedelta
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from typing import Any

from app.core.security import create_access_token
from app.core.config import settings
from app.db.session import get_db
from app.schemas.user import UserCreate, UserOut, Token 
from app.services import auth_service
from app.services.auth_service import get_current_superadmin_user
from app.models.user import RoleEnum, User  # Importamos el Enum para estar seguros

router = APIRouter()

@router.post("/login", response_model=Token)
def login_access_token(
    db: Session = Depends(get_db), form_data: OAuth2PasswordRequestForm = Depends()
) -> Any:
    user = auth_service.authenticate_user(
        db, username=form_data.username, password=form_data.password
    )
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        subject=user.username, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}

@router.post("/register", response_model=UserOut)
def register_user(
    *,
    db: Session = Depends(get_db),
    user_in: UserCreate,
) -> Any:
    user = auth_service.get_user_by_username(db, username=user_in.username)
    if user:
        raise HTTPException(
            status_code=400,
            detail="The user with this username already exists in the system.",
        )
    
    # --- BLOQUEO DE SEGURIDAD AQUÍ ---
    # Forzamos que el rol sea siempre 'user', ignorando lo que el cliente envíe
    user_in.role = RoleEnum.user 
    # ---------------------------------
    
    user = auth_service.create_user(db, user=user_in)
    return user

@router.get("/me", response_model=UserOut)
def read_current_user(
    current_user: Any = Depends(auth_service.get_current_active_user),
) -> Any:
    return current_user

@router.post("/create-admin", response_model=UserOut)
def create_admin(
    *,
    db: Session = Depends(get_db),
    user_in: UserCreate,
    current_admin: User = Depends(get_current_superadmin_user),
) -> Any:
    """
    Create a new superadmin. Only a superadmin can do this.
    """
    user = auth_service.get_user_by_username(db, username=user_in.username)
    if user:
        raise HTTPException(
            status_code=400,
            detail="The user with this username already exists in the system.",
        )
    
    # Forzamos que el rol sea superadmin
    user_in.role = RoleEnum.superadmin
    
    user = auth_service.create_user(db, user=user_in)
    return user