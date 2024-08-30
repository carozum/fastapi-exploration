
from sqlalchemy.orm.session import Session
from db.models import DbUser
from schemas import UserBase
from db.hash import Hash
from fastapi import HTTPException, status

############################################
# 5 Création des actions dans la bdd (on n'est plus au niveau du schéma. )


def create_user(db: Session, request: UserBase):
    new_user = DbUser(
        username=request.username,
        email=request.email,
        # hashé !!
        password=Hash.hash_password(request.password)
    )
    try:
        db.add(new_user)
        db.commit()          # sert à mettre à jour la table
        db.refresh(new_user)  # sert à récupérer dans l'appli le new user.
        return new_user
    except Exception as error:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Username or email already registered"
        )
