from fastapi import APIRouter, Depends
from schemas import UserBase, UserDisplay
from db.database import get_db
from sqlalchemy.orm.session import Session
from db import db_user

router = APIRouter(
    prefix="/user",
    tags=['user']
)

# Création d'une route pour créer un utilisateur dans mon api
# validateur intermédiaire : le schéma (dépend de pydantic)


@router.post('/', response_model=UserDisplay)
def create_user(request: UserBase, db: Session = Depends(get_db)):
    db_user.create_user(db, request)
