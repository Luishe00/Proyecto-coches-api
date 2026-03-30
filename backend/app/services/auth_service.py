from datetime import timedelta
from typing import Optional, Union
from jose import JWTError, jwt
from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session

from app.core.config import settings
from app.core.security import get_password_hash, verify_password, create_access_token
from app.core.exceptions import ConflictError, CredentialsError, PermissionDeniedError
from app.db.session import get_db
from app.schemas.user import UserCreate
from app.repositories.user_repository import IUserRepository, SQLAlchemyUserRepository
from app.domain import entities as domain

oauth2_scheme = OAuth2PasswordBearer(tokenUrl=f"{settings.API_V1_STR}/auth/login")

def get_user_repository(db: Session = Depends(get_db)) -> IUserRepository:
    return SQLAlchemyUserRepository(db)

def create_user(repository: IUserRepository, user_in: UserCreate) -> domain.User:
    if repository.get_by_username(user_in.username):
        raise ConflictError(detail="The user with this username already exists in the system.")
    
    user_in.role = domain.RoleEnum.user
    hashed_password = get_password_hash(user_in.password)
    return repository.create(
        username=user_in.username,
        hashed_password=hashed_password,
        role=user_in.role
    )

def create_admin(repository: IUserRepository, user_in: UserCreate) -> domain.User:
    if repository.get_by_username(user_in.username):
        raise ConflictError(detail="The user with this username already exists in the system.")
    
    user_in.role = domain.RoleEnum.superadmin
    hashed_password = get_password_hash(user_in.password)
    return repository.create(
        username=user_in.username,
        hashed_password=hashed_password,
        role=user_in.role
    )

def login_for_access_token(repository: IUserRepository, username: str, password: str) -> dict:
    user = authenticate_user(repository, username=username, password=password)
    if not user:
        raise CredentialsError(detail="Incorrect username or password")
    
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        subject=user.username, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}

def authenticate_user(repository: IUserRepository, username: str, password: str) -> Optional[domain.User]:
    user = repository.get_by_username(username)
    if not user or not verify_password(password, user.hashed_password):
        return None
    return user

async def get_current_user(
    repository: IUserRepository = Depends(get_user_repository), 
    token: str = Depends(oauth2_scheme)
) -> domain.User:
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise CredentialsError()
    except JWTError:
        raise CredentialsError()
    
    user = repository.get_by_username(username=username)
    if user is None:
        raise CredentialsError()
    return user

async def get_current_active_user(current_user: domain.User = Depends(get_current_user)) -> domain.User:
    return current_user

async def get_current_active_superadmin(current_user: domain.User = Depends(get_current_active_user)) -> domain.User:
    if current_user.role != domain.RoleEnum.superadmin:
        raise PermissionDeniedError()
    return current_user
