from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from app.core.config import settings

# Añadimos pool_recycle para XAMPP
engine = create_engine(
    settings.DATABASE_URL, 
    pool_pre_ping=True,
    pool_recycle=3600  # Refresca la conexión cada hora
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()