from sqlalchemy.orm import DeclarativeBase, mapped_column
from typing import Optional
from pydantic import BaseModel
from sqlalchemy import String, Boolean, Integer

class Base(DeclarativeBase):
    pass

class Todo(Base):
    __tablename__ = "todos"
    id = mapped_column(Integer, primary_key=True)
    title = mapped_column(String(100), nullable=False)
    description = mapped_column(String(100), nullable=False)
    completed = mapped_column(Boolean, nullable=False)
    priority = mapped_column(String(100), nullable=False)

class User(Base):
    __tablename__ = "users"
    id = mapped_column(Integer, primary_key=True)
    username = mapped_column(String(100), nullable=False, unique=True)
    email = mapped_column(String(100), nullable=False, unique=True)
    password_hashed = mapped_column(String(100), nullable=False)
    is_active = mapped_column(Boolean, nullable=False, default=True)






class Token(BaseModel):
    access_token: str
    token_type: str
 
class TokenData(BaseModel):
    username: Optional[str] = None