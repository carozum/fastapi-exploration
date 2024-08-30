from .database import Base
from sqlalchemy import Column, Integer, String

########################################################
# 2 création des tables les modèles


class DbUser(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True)
    email = Column(String, unique=True)
    password = Column(String)
