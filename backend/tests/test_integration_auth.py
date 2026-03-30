import pytest
from sqlalchemy.orm import Session
from app.repositories.user_repository import SQLAlchemyUserRepository
from app.domain.entities import RoleEnum
from app.core.security import get_password_hash

def test_integration_create_user(db_session: Session):
    """Verifica la creación y persistencia de un usuario real."""
    repo = SQLAlchemyUserRepository(db_session)
    username = "integration_user"
    hashed = get_password_hash("secret")
    
    # Crear
    user = repo.create(username=username, hashed_password=hashed, role=RoleEnum.user)
    db_session.commit()
    
    assert user.id is not None
    assert user.username == username
    
    # Recuperar
    db_session.expire_all()
    found = repo.get_by_username(username)
    assert found is not None
    assert found.id == user.id

def test_integration_get_non_existent_user(db_session: Session):
    """Verifica el comportamiento del repositorio ante usuarios inexistentes."""
    repo = SQLAlchemyUserRepository(db_session)
    found = repo.get_by_username("non_existent_ghost")
    assert found is None

def test_integration_create_superadmin(db_session: Session):
    """Valida la creación de usuarios con roles específicos."""
    repo = SQLAlchemyUserRepository(db_session)
    user = repo.create(username="admin_integ", hashed_password="pw", role=RoleEnum.superadmin)
    db_session.commit()
    
    assert user.role == RoleEnum.superadmin
