from fastapi.param_functions import Depends
from fastapi.security import OAuth2PasswordBearer
from typing import Optional
from datetime import datetime, timedelta, timezone
import jwt

from sqlalchemy.orm import Session
from database import get_db
from fastapi import HTTPException, status
from routers import readers


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# openssl rand -hex 32
SECRET_KEY = 'bae01ea69fed22551eabadaae29239d747f5dbc5c5d142516dab6d19373b7d10'
ALGORITHM = 'HS256'
ACCESS_TOKEN_EXPIRE_MINUTES = 30


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail='Could not validate credentials',
        headers={"WWW-Authenticate": "Bearer"}
    )

    payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    email: str = payload.get("sub")
    if email is None:
        raise credentials_exception

    user = readers.get_user_by_email(db, email)

    if user is None:
        raise credentials_exception

    return user
