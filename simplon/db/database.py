from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

###########################################
# 1 définition du moteur de la BDD

SQLALCHEMY_DATABASE_URL = "sqlite:///./fastapi-practice.db"

# moteur SQL
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
# création de la session sur le moteur
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


def get_db():
    # pour récupérer la base de données
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
