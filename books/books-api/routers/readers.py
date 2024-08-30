
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
    prefix="/readers",
    tags=['readers']
)


@router.post("/", response_model=schemas.Reader)
def create_reader(
        reader: schemas.ReaderCreate,
        db: Session = Depends(get_db)):
    """ Créer un lecteur"""
    db_reader = crud.get_reader_by_email(db, email=reader.email)
    if db_reader:
        raise HTTPException(status_code=400, detail="Email already registered")
    return crud.create_reader(db=db, reader=reader)


@router.get("/{reader_id}/loans/", response_model=List[schemas.Loan])
def get_loans_for_reader(
        reader_id: int,
        db: Session = Depends(get_db)):
    """voir la liste des emprunts pour un lecteur en fonction de son id"""
    return crud.get_loans_by_reader(db=db, reader_id=reader_id)
