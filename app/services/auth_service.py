from sqlalchemy.orm import Session
from app.models.user import User, RoleEnum
from app.schemas.user import UserCreate
from app.core.security import get_password_hash, verify_password
from fastapi.security import OAuth2PasswordBearer
from fastapi import Depends, HTTPException, status
from app.db.session import get_db
from jose import JWTError, jwt
from app.core.config import settings

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="api/v1/auth/login")


def get_user_by_username(db: Session, username: str) -> User | None:
    return db.query(User).filter(User.username == username).first()


def create_user(db: Session, user: UserCreate) -> User:
    hashed_password = get_password_hash(user.password)
    db_user = User(
        username=user.username,
        hashed_password=hashed_password,
        role=user.role
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def authenticate_user(db: Session, username: str, password: str) -> User | bool:
    user = get_user_by_username(db, username)
    if not user:
        return False
    
    if not verify_password(password, user.hashed_password):
        return False
        
    return user


async def get_current_user(
    db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)
) -> User:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    
    user = get_user_by_username(db, username=username)
    if user is None:
        raise credentials_exception
    return user


async def get_current_active_user(current_user: User = Depends(get_current_user)) -> User:
    return current_user


async def get_current_superadmin_user(current_user: User = Depends(get_current_active_user)) -> User:
    if current_user.role != RoleEnum.superadmin:
        raise HTTPException(status_code=403, detail="The user doesn't have enough privileges")
    return current_user
