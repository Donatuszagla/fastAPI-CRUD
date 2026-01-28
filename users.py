from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
import jwt
from jwt.exceptions import InvalidTokenError
from pwdlib import PasswordHash
from sqlalchemy import select
from sqlalchemy.orm import Session
from typing import Optional
from db import engine
from models import User
from datetime import datetime, timedelta

user_router = APIRouter()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/token")

def verify_password(plain_password, hashed_password):
    return PasswordHash.recommended().verify(password=plain_password, hash=hashed_password)

def get_password_hash(password: str):
    return PasswordHash.recommended().hash(password=password)

def find_user(session: Session, email: str):
    return session.execute(select(User).where(User.email == email)).scalar()

def authenticate_user(session: Session, email: str, password: str):
    user = find_user(session, email)
    if not user:
        print(f"User not found for email: {email}")
        return False
    if not verify_password(password, user.password_hashed):   
        print(f"Invalid password for user: {email}")
        return False
    return user

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, "secret", algorithm="HS256")
    return encoded_jwt

async def get_current_user(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=401,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, "secret", algorithms=["HS256"])
        email: str = payload.get("sub")
        if email is None:
            raise credentials_exception
    except InvalidTokenError:
        raise credentials_exception
    with Session(engine) as session:
        user = find_user(session, email=email)
    if user is None:
        raise credentials_exception
    return user

async def get_current_active_user(current_user: User = Depends(get_current_user)):
    if not current_user.is_active:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user

    