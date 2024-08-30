
from fastapi import status, Response, APIRouter, Depends, HTTPException
from sqlalchemy.orm.session import Session
from database import get_db
import crud
from typing import List

from enum import Enum
from typing import Optional
import schemas

router = APIRouter(
    prefix="/books",
    tags=['books']
)


@router.post("/", response_model=schemas.Book)
# créer les livres
def create_book(book: schemas.BookCreate, db: Session = Depends(get_db)):
    return crud.create_book(db=db, book=book)


@router.get("/", response_model=List[schemas.Book])
# liste de tous les livres
def get_books(db: Session = Depends(get_db)):
    return crud.get_books(db=db)


@router.get("/available/", response_model=List[schemas.Book])
def get_available_books(db: Session = Depends(get_db)):
    # liste des livres qui ne sont pas empruntés
    return crud.get_available_books(db=db)
