import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from sqlalchemy.orm import Session
from app.db.session import SessionLocal, engine, Base
from app.models.car import Car
from app.models.user import User, RoleEnum
from app.core.security import get_password_hash

# Create tables if not exist
Base.metadata.create_all(bind=engine)

def seed_data():
    db: Session = SessionLocal()
    try:
        # Clear existing data
        db.query(Car).delete()
        db.query(User).delete()
        db.commit()

        # Seed Users
        superadmin = User(
            username="admin",
            hashed_password=get_password_hash("admin123"),
            role=RoleEnum.superadmin
        )
        normal_user = User(
            username="user",
            hashed_password=get_password_hash("user123"),
            role=RoleEnum.user
        )
        db.add_all([superadmin, normal_user])
        db.commit()

        # Seed Cars (24 cars total)
        cars_data = [
            # Ferrari
            {"marca": "Ferrari", "modelo": "488 GTB", "anio_fabricacion": 2016, "cv": 670, "peso": 1370, "velocidad_max": 330, "precio": 250000},
            {"marca": "Ferrari", "modelo": "F8 Tributo", "anio_fabricacion": 2020, "cv": 720, "peso": 1435, "velocidad_max": 340, "precio": 276000},
            {"marca": "Ferrari", "modelo": "SF90 Stradale", "anio_fabricacion": 2021, "cv": 1000, "peso": 1570, "velocidad_max": 340, "precio": 500000},
            {"marca": "Ferrari", "modelo": "Roma", "anio_fabricacion": 2020, "cv": 620, "peso": 1570, "velocidad_max": 320, "precio": 220000},
            
            # Porsche
            {"marca": "Porsche", "modelo": "911 Carrera S", "anio_fabricacion": 2019, "cv": 450, "peso": 1515, "velocidad_max": 308, "precio": 130000},
            {"marca": "Porsche", "modelo": "Taycan Turbo S", "anio_fabricacion": 2020, "cv": 761, "peso": 2295, "velocidad_max": 260, "precio": 185000},
            {"marca": "Porsche", "modelo": "Panamera GTS", "anio_fabricacion": 2021, "cv": 480, "peso": 2020, "velocidad_max": 300, "precio": 140000},
            {"marca": "Porsche", "modelo": "Cayenne Turbo", "anio_fabricacion": 2018, "cv": 550, "peso": 2175, "velocidad_max": 286, "precio": 135000},

            # BMW
            {"marca": "BMW", "modelo": "M3 Competition", "anio_fabricacion": 2021, "cv": 510, "peso": 1730, "velocidad_max": 290, "precio": 85000},
            {"marca": "BMW", "modelo": "M5 CS", "anio_fabricacion": 2022, "cv": 635, "peso": 1825, "velocidad_max": 305, "precio": 142000},
            {"marca": "BMW", "modelo": "X5 M", "anio_fabricacion": 2020, "cv": 600, "peso": 2310, "velocidad_max": 250, "precio": 105000},
            {"marca": "BMW", "modelo": "i4 M50", "anio_fabricacion": 2022, "cv": 544, "peso": 2215, "velocidad_max": 225, "precio": 65000},

            # Audi
            {"marca": "Audi", "modelo": "RS e-tron GT", "anio_fabricacion": 2021, "cv": 646, "peso": 2347, "velocidad_max": 250, "precio": 140000},
            {"marca": "Audi", "modelo": "R8 V10 Performance", "anio_fabricacion": 2019, "cv": 620, "peso": 1595, "velocidad_max": 331, "precio": 195000},
            {"marca": "Audi", "modelo": "RS6 Avant", "anio_fabricacion": 2020, "cv": 600, "peso": 2075, "velocidad_max": 305, "precio": 110000},
            {"marca": "Audi", "modelo": "RSQ8", "anio_fabricacion": 2020, "cv": 600, "peso": 2315, "velocidad_max": 305, "precio": 115000},

            # Toyota
            {"marca": "Toyota", "modelo": "GR Yaris", "anio_fabricacion": 2020, "cv": 261, "peso": 1280, "velocidad_max": 230, "precio": 35000},
            {"marca": "Toyota", "modelo": "GR Supra", "anio_fabricacion": 2019, "cv": 340, "peso": 1495, "velocidad_max": 250, "precio": 52000},
            {"marca": "Toyota", "modelo": "RAV4 Hybrid", "anio_fabricacion": 2021, "cv": 218, "peso": 1590, "velocidad_max": 180, "precio": 38000},
            {"marca": "Toyota", "modelo": "Corolla GR", "anio_fabricacion": 2023, "cv": 300, "peso": 1475, "velocidad_max": 230, "precio": 40000},

            # Tesla
            {"marca": "Tesla", "modelo": "Model S Plaid", "anio_fabricacion": 2021, "cv": 1020, "peso": 2162, "velocidad_max": 322, "precio": 130000},
            {"marca": "Tesla", "modelo": "Model 3 Performance", "anio_fabricacion": 2022, "cv": 513, "peso": 1844, "velocidad_max": 261, "precio": 55000},
            {"marca": "Tesla", "modelo": "Model X Plaid", "anio_fabricacion": 2022, "cv": 1020, "peso": 2455, "velocidad_max": 262, "precio": 138000},
            {"marca": "Tesla", "modelo": "Model Y Long Range", "anio_fabricacion": 2021, "cv": 351, "peso": 2003, "velocidad_max": 217, "precio": 50000},
        ]

        db_cars = [Car(**data) for data in cars_data]
        db.add_all(db_cars)
        db.commit()

        print("Database seeded successfully with 2 users and 24 cars!")
        print("Superadmin: admin / admin123")
        print("User: user / user123")

    except Exception as e:
        db.rollback()
        print(f"Error seeding database: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    seed_data()
