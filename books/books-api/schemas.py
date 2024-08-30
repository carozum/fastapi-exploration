from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import List, Optional

############################################
# 3. Schéma de validation de l'API

# input validation


class ReaderCreate(BaseModel):
    nom: str
    prenom: str
    email: EmailStr
    password: str

# output validation


class Reader(BaseModel):
    id: int
    nom: str
    prenom: str
    email: EmailStr
    books: List[int] = []

    class Config:
        orm_mode = True

# input validation


class BookCreate(BaseModel):
    titre: str
    auteur: str
    isbn: str

# output validation


class Book(BaseModel):
    id: int
    titre: str
    auteur: str
    isbn: str

    class Config:
        orm_mode = True

# input validation


class LoanCreate(BaseModel):
    reader_id: int
    book_id: int


# output validation


class Loan(BaseModel):
    id: int
    reader_id: int
    book_id: int
    date_emprunt: datetime
    date_retour: Optional[datetime] = None

    class Config:
        orm_mode = True
        json_encoders = {
            datetime: lambda v: v.strftime('%d-%m-%Y'),
        }
