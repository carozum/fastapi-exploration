from fastapi import APIRouter, HTTPException, status
from fastapi.param_functions import Depends
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from sqlalchemy.orm.session import Session
from database import get_db
import models
from hash import Hash
from auth import oauth2
import schemas

router = APIRouter(
    tags=['authentication']
)


@router.get("/profile", response_model=schemas.Reader)
def get_profile(current_user: models.Reader = Depends(oauth2.get_current_user)):
    """
    Get the profile of the currently authenticated user.
    """
    return current_user


@router.post('/token')
def get_token(request: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = db.query(models.Reader).filter(
        models.Reader.email == request.username).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Invalid credentials")
    if not Hash.verify_password(user.hashed_password, request.password):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Incorrect password")

    access_token = oauth2.create_access_token(data={'sub': user.email})

    return {
        'access_token': access_token,
        'token_type': 'bearer',
        'user_id': user.id,
        'email': user.email
    }
