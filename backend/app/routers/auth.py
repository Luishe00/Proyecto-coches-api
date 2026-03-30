from fastapi import APIRouter, Depends, status
from fastapi.security import OAuth2PasswordRequestForm
from app.schemas.user import UserCreate, UserOut, Token 
from app.services import auth_service
from app.repositories.user_repository import IUserRepository
from app.domain.entities import User

router = APIRouter()

@router.post("/login", response_model=Token)
def login_access_token(
    repository: IUserRepository = Depends(auth_service.get_user_repository),
    form_data: OAuth2PasswordRequestForm = Depends()
):
    """
    OAuth2 compatible token login, get an access token for future requests.
    """
    return auth_service.login_for_access_token(
        repository, username=form_data.username, password=form_data.password
    )

@router.post("/register", response_model=UserOut)
def register_user(
    repository: IUserRepository = Depends(auth_service.get_user_repository),
    user_in: UserCreate = None,
):
    """
    Create a new user.
    """
    return auth_service.create_user(repository, user_in=user_in)

@router.get("/me", response_model=UserOut)
def read_current_user(
    current_user: User = Depends(auth_service.get_current_active_user),
):
    """
    Get current user.
    """
    return current_user

@router.post("/create-admin", response_model=UserOut)
def create_admin(
    user_in: UserCreate,
    repository: IUserRepository = Depends(auth_service.get_user_repository),
    current_admin: User = Depends(auth_service.get_current_active_superadmin),
):
    """
    Create a new superadmin. Only a superadmin can do this.
    """
    return auth_service.create_admin(repository, user_in=user_in)