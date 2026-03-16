import pytest
from httpx import AsyncClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.main import app
from app.db.session import Base, get_db
from app.core.security import get_password_hash
from app.models.user import User, RoleEnum
from app.models.car import Car

# Use a test database or sqlite in-memory for testing
# We'll use sqlite for isolated, fast tests without needing MySQL setup
SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

@pytest.fixture(scope="module")
def db_session():
    Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()
    
    # Seed minimal data for tests
    superadmin = User(username="admin_test", hashed_password=get_password_hash("test"), role=RoleEnum.superadmin)
    normal_user = User(username="user_test", hashed_password=get_password_hash("test"), role=RoleEnum.user)
    
    test_car1 = Car(marca="Toyota", modelo="Corolla", anio_fabricacion=2020, cv=120, peso=1300, velocidad_max=200, precio=25000)
    test_car2 = Car(marca="BMW", modelo="M3", anio_fabricacion=2021, cv=510, peso=1730, velocidad_max=290, precio=85000)
    
    db.add_all([superadmin, normal_user, test_car1, test_car2])
    db.commit()
    
    yield db
    
    db.close()
    Base.metadata.drop_all(bind=engine)

from httpx import AsyncClient, ASGITransport

@pytest.fixture(scope="module")
def client(db_session):
    def override_get_db():
        try:
            yield db_session
        finally:
            pass
            
    app.dependency_overrides[get_db] = override_get_db
    transport = ASGITransport(app=app)
    with AsyncClient(transport=transport, base_url="http://test") as c:
        yield c
    app.dependency_overrides.clear()

@pytest.fixture(scope="module")
async def superadmin_token_headers(client: AsyncClient):
    response = await client.post(
        "/api/v1/auth/login",
        data={"username": "admin_test", "password": "test"}
    )
    token = response.json()["access_token"]
    return {"Authorization": f"Bearer {token}"}

@pytest.fixture(scope="module")
async def user_token_headers(client: AsyncClient):
    response = await client.post(
        "/api/v1/auth/login",
        data={"username": "user_test", "password": "test"}
    )
    token = response.json()["access_token"]
    return {"Authorization": f"Bearer {token}"}
