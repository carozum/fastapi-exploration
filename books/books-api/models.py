########################################################
# 2 création des tables les modèles

from sqlalchemy.orm import relationship
from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from database import Base
from sqlalchemy import Column, Integer, String


class Reader(Base):
    __tablename__ = 'readers'
    id = Column(Integer, primary_key=True, index=True)
    nom = Column(String, index=True)
    prenom = Column(String, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    books = relationship("Book", secondary="loans")


class Book(Base):
    __tablename__ = 'books'
    id = Column(Integer, primary_key=True, index=True)
    titre = Column(String, index=True)
    auteur = Column(String, index=True)
    isbn = Column(String, unique=True, index=True)


class Loan(Base):
    __tablename__ = "loans"
    id = Column(Integer, primary_key=True, index=True)
    reader_id = Column(Integer, ForeignKey("readers.id"))
    book_id = Column(Integer, ForeignKey("books.id"))
    date_emprunt = Column(DateTime, nullable=True)
    date_retour = Column(DateTime, nullable=True)
