from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import os

# DATABASE_URL = "postgresql://user:password@order-db-service:5432/orderdb"

DB_USER = os.environ.get("POSTGRES_USER")
DB_PASSWORD = os.environ.get("POSTGRES_PASSWORD")

DATABASE_URL = f"cockroachdb://{DB_USER}:{DB_PASSWORD}@valley-werefox-14325.j77.aws-ap-south-1.cockroachlabs.cloud:26257/orders"

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
