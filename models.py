from sqlmodel import SQLModel, Field
from typing import Optional
from pydantic import EmailStr, BaseModel


class Todo(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    title: str = Field(..., max_length=100)
    description: str
    completed: bool
    priority: str

class User(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    username: str = Field(..., min_length=3, max_length=100, unique=True)
    email: EmailStr
    password_hashed: str
    is_active: bool = True






class Token(BaseModel):
    access_token: str
    token_type: str
 
class TokenData(BaseModel):
    username: Optional[str] = None