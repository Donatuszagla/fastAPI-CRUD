from fastapi import APIRouter
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
import jwt
from jwt.exceptions import InvalidTokenError
from pwdlib import PasswordHash
from sqlmodel import SQLModel, Field, create_engine, select, Session
from typing import Optional
import main
from pydantic import BaseModel

router = APIRouter()

class UserOutput(BaseModel):
    id: int
    username: str = Field(..., max_length=100)
    email: str

class User(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    username: str = Field(..., max_length=100)
    email: str
    password_hashed: str



def verify_password(plain_password, hashed_password):
    return PasswordHash.recommended().verify(password=plain_password, hash=hashed_password)

def get_password_hash(password: str):
    return PasswordHash.recommended().hash(password=password)

@router.post("/users", tags=["users"])
def create_user(user: User):
    try:
        user_data = user.model_dump(exclude_unset=True)
        user_data["password_hashed"] = get_password_hash(user_data["password_hashed"])
        user = User(**user_data)
        with Session(main.engine) as session:
            session.add(user)
            session.commit()
            session.refresh(user)
            return {"message": "User created successfully",
            "user": UserOutput(**user.model_dump())}
    except Exception as e:
        return {"error": str(e)}

@router.get("/users", tags=["users"])
def get_users():
    try:
        with Session(main.engine) as session:
            users = session.exec(select(User)).all()
        return [UserOutput(**user.model_dump()) for user in users]
    except Exception as e:
        return {"error": str(e)}

@router.get("/users/{user_id}", tags=["users"])
def get_user(user_id: int):
    try:
        with Session(main.engine) as session:
            user = session.get(User, user_id)
        return UserOutput(**user.model_dump())
    except Exception as e:
        return {"error": str(e)}

@router.put("/users/{user_id}", tags=["users"])
def update_user(user_id: int, user: User):
    try:
        with Session(main.engine) as session:
            stored_user = session.get(User, user_id)
            new_data = user.model_dump(exclude_unset=True)
            updated_user = stored_user.model_copy(update=new_data)
            session.add(updated_user)
            session.commit()
            session.refresh(updated_user)
        return UserOutput(**updated_user.model_dump())
    except Exception as e:
        return {"error": str(e)}

@router.delete("/users/{user_id}", tags=["users"])
def delete_user(user_id: int):
    try:
        with Session(main.engine) as session:
            user = session.get(User, user_id)
            session.delete(user)
            session.commit()
        return {"message": "User deleted successfully"}
    except Exception as e:
        return {"error": str(e)}

