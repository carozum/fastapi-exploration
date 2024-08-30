
from fastapi import status, Response, APIRouter, Depends, HTTPException
from sqlalchemy.orm.session import Session
from database import get_db
import crud
from typing import List

from enum import Enum
from typing import Optional
import schemas
import models


router = APIRouter(
    prefix="/loans",
    tags=['loans']
)


@router.post("/", response_model=schemas.Loan)
def create_loan(
        loan: schemas.LoanCreate,
        db: Session = Depends(get_db)):
    """Permet à un lecteur d'emprunter un livre avec un check si le livre est déjà emprunté"""
    db_loan = crud.get_loan_by_book(db=db, book_id=loan.book_id)
    if db_loan:
        raise HTTPException(status_code=400, detail="Book already loaned")
    return crud.create_loan(db=db, loan=loan)


@router.put("/loans/{loan_id}/return", response_model=schemas.Loan)
def return_book(loan_id: int, db: Session = Depends(get_db)):
    """ Faire le retour d'un livre emprunté par un utilisateur"""
    return crud.return_book(db=db, loan_id=loan_id)
