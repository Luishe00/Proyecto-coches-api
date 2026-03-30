import pytest
from pydantic import ValidationError
from unittest.mock import MagicMock
from jose import jwt
from app.services import auth_service
from app.repositories.user_repository import IUserRepository
from app.domain.entities import User, RoleEnum
from app.schemas.user import UserCreate
from app.core.exceptions import ConflictError, CredentialsError, PermissionDeniedError
from app.core.security import get_password_hash, create_access_token
from app.core.config import settings

@pytest.fixture
def mock_repo():
    return MagicMock(spec=IUserRepository)

def test_create_user_success(mock_repo):
    user_in = UserCreate(username="testuser", password="password123")
    mock_repo.get_by_username.return_value = None
    
    fake_user = User(id=1, username="testuser", hashed_password="hashed_password", role=RoleEnum.user)
    mock_repo.create.return_value = fake_user

    result = auth_service.create_user(mock_repo, user_in)

    assert result == fake_user
    mock_repo.get_by_username.assert_called_once_with("testuser")
    mock_repo.create.assert_called_once()

def test_create_user_conflict(mock_repo):
    user_in = UserCreate(username="testuser", password="password123")
    existing_user = User(id=1, username="testuser", hashed_password="hashed", role=RoleEnum.user)
    mock_repo.get_by_username.return_value = existing_user

    with pytest.raises(ConflictError):
        auth_service.create_user(mock_repo, user_in)
    mock_repo.create.assert_not_called()

def test_create_admin_success(mock_repo):
    user_in = UserCreate(username="adminuser", password="password123")
    mock_repo.get_by_username.return_value = None
    
    fake_user = User(id=1, username="adminuser", hashed_password="hashed_password", role=RoleEnum.superadmin)
    mock_repo.create.return_value = fake_user

    result = auth_service.create_admin(mock_repo, user_in)

    assert result == fake_user
    mock_repo.create.assert_called_once()

def test_authenticate_user_success(mock_repo):
    password = "password123"
    hashed = get_password_hash(password)
    fake_user = User(id=1, username="testuser", hashed_password=hashed, role=RoleEnum.user)
    mock_repo.get_by_username.return_value = fake_user

    result = auth_service.authenticate_user(mock_repo, "testuser", password)
    assert result == fake_user

def test_authenticate_user_fail_wrong_password(mock_repo):
    password = "correct_password"
    hashed = get_password_hash(password)
    fake_user = User(id=1, username="testuser", hashed_password=hashed, role=RoleEnum.user)
    mock_repo.get_by_username.return_value = fake_user

    result = auth_service.authenticate_user(mock_repo, "testuser", "wrong_password")
    assert result is None

def test_authenticate_user_fail_not_found(mock_repo):
    mock_repo.get_by_username.return_value = None
    result = auth_service.authenticate_user(mock_repo, "ghost", "password")
    assert result is None

def test_login_for_access_token_success(mock_repo):
    password = "password123"
    hashed = get_password_hash(password)
    fake_user = User(id=1, username="testuser", hashed_password=hashed, role=RoleEnum.user)
    mock_repo.get_by_username.return_value = fake_user

    result = auth_service.login_for_access_token(mock_repo, "testuser", password)
    assert "access_token" in result
    assert result["token_type"] == "bearer"

def test_login_for_access_token_fail(mock_repo):
    mock_repo.get_by_username.return_value = None
    with pytest.raises(CredentialsError):
        auth_service.login_for_access_token(mock_repo, "testuser", "wrong")

@pytest.mark.asyncio
async def test_get_current_user_success(mock_repo):
    fake_user = User(id=1, username="testuser", hashed_password="hashed", role=RoleEnum.user)
    mock_repo.get_by_username.return_value = fake_user
    token = create_access_token("testuser")

    result = await auth_service.get_current_user(mock_repo, token)
    assert result == fake_user

@pytest.mark.asyncio
async def test_get_current_user_invalid_token(mock_repo):
    with pytest.raises(CredentialsError):
        await auth_service.get_current_user(mock_repo, "invalid.token.string")

@pytest.mark.asyncio
async def test_get_current_user_no_sub(mock_repo):
    # Crear token estructurado pero sin 'sub'
    token = jwt.encode({"other": "data"}, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    with pytest.raises(CredentialsError):
        await auth_service.get_current_user(mock_repo, token)

@pytest.mark.asyncio
async def test_get_current_user_not_found_in_db(mock_repo):
    mock_repo.get_by_username.return_value = None
    token = create_access_token("ghost")
    with pytest.raises(CredentialsError):
        await auth_service.get_current_user(mock_repo, token)

@pytest.mark.asyncio
async def test_get_current_active_user():
    fake_user = User(id=1, username="u", hashed_password="pw", role=RoleEnum.user)
    res = await auth_service.get_current_active_user(fake_user)
    assert res == fake_user

@pytest.mark.asyncio
async def test_get_current_active_superadmin_success():
    fake_user = User(id=1, username="admin", hashed_password="pw", role=RoleEnum.superadmin)
    res = await auth_service.get_current_active_superadmin(fake_user)
    assert res == fake_user

@pytest.mark.asyncio
async def test_get_current_active_superadmin_fail():
    fake_user = User(id=1, username="u", hashed_password="pw", role=RoleEnum.user)
    with pytest.raises(PermissionDeniedError):
        await auth_service.get_current_active_superadmin(fake_user)

# --- BLACK-BOX: Equivalence Classes ---
def test_user_create_password_valid_length():
    user = UserCreate(username="test", password="a" * 72)
    assert user.password == "a" * 72

def test_user_create_password_invalid_length():
    with pytest.raises(ValidationError):
        UserCreate(username="test", password="a" * 73)

# --- BLACK-BOX: Decision Tables ---
@pytest.mark.parametrize("user_exists, password_correct, expected_result", [
    (True, True, "user"),
    (True, False, None),
    (False, None, None)
])
def test_authenticate_user_decision_table(mock_repo, user_exists, password_correct, expected_result):
    password = "password123"
    hashed = get_password_hash(password)
    fake_user = User(id=1, username="testuser", hashed_password=hashed, role=RoleEnum.user)
    
    if user_exists:
        mock_repo.get_by_username.return_value = fake_user
    else:
        mock_repo.get_by_username.return_value = None
        
    pwd_to_check = password if password_correct else "wrong_password"
    
    result = auth_service.authenticate_user(mock_repo, "testuser", pwd_to_check)
    
    if expected_result == "user":
        assert result == fake_user
    else:
        assert result is None
