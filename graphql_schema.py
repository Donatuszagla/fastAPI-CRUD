from users import get_password_hash
import strawberry
from typing import List, Optional
from fastapi import Request
from users import get_current_user
from models import Todo, User
from db import engine
from sqlalchemy.orm import Session
from sqlalchemy import select
from fastapi import HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from users import authenticate_user, create_access_token
from datetime import timedelta


@strawberry.type
class UserType:
    id: int
    username: str
    email: str
    is_active: bool

@strawberry.type
class TokenType:
    access_token: str
    token_type: str


@strawberry.type
class TodoType:
    id: int
    title: str
    description: str
    completed: bool
    priority: str


@strawberry.input
class UserInputType(UserType):
    password: str


@strawberry.input
class UserAuthForm:
    email: str
    password: str

async def get_context(request: Request):
    user = None
    auth = request.headers.get("Authorization")

    if auth:
        token = auth.replace("Bearer ", "")
        try:
            user = await get_current_user(token)
        except:
            pass

    return {
        "request": request,
        "user": user
    }



@strawberry.type
class Query:
    @strawberry.field
    def todos(self) -> List[TodoType]:
        with Session(engine) as session:
            todos = session.execute(select(Todo)).scalars().all()
        return todos
    
    @strawberry.field
    def todo(self, todoId: int) -> TodoType:
        with Session(engine) as session:
            todo = session.get(Todo, todoId)
        return todo

    @strawberry.field
    def get_users(self) -> List[UserType]:
        try:
            with Session(engine) as session:
                users = session.execute(select(User)).scalars().all()
            return users
        except Exception as e:
            raise HTTPException(status_code=404, detail="User not found")

    @strawberry.field
    async def get_user(self, userId: int) -> UserType:
        try:
            with Session(engine) as session:
                user = session.execute(select(User).where(User.id == userId)).scalar()
            return user
        except Exception as e:
            raise HTTPException(status_code=404, detail="User not found")

@strawberry.type
class Mutation:
    @strawberry.field
    def create_todo(self, info, title: str, description: str, completed: bool, priority: str) -> TodoType:
        print(info.context)
        current_user = info.context["user"]
        if not current_user:
            raise HTTPException(status_code=401, detail="Unauthorized")
        with Session(engine) as session:
            todo = Todo(title=title, description=description, completed=completed, priority=priority)
            session.add(todo)
            session.commit()    
            session.refresh(todo)
        return todo

    @strawberry.field
    def update_todo(self, info, todoId: int, title: str, description: str, completed: bool, priority: str) -> TodoType:
        current_user = info.context["user"]
        if not current_user:
            raise HTTPException(status_code=401, detail="Unauthorized")
        with Session(engine) as session:
            todo = session.get(Todo, todoId)
            todo.title = title
            todo.description = description
            todo.completed = completed
            todo.priority = priority    
            session.add(todo)
            session.commit()
            session.refresh(todo)
        return todo

    @strawberry.field
    def delete_todo(self, info, todoId: int) -> TodoType:
        current_user = info.context["user"]
        if not current_user:
            raise HTTPException(status_code=401, detail="Unauthorized")
        with Session(engine) as session:
            todo = session.get(Todo, todoId)
            session.delete(todo)
            session.commit()
        return todo

    @strawberry.field
    async def create_user(self, UserId: int, username: str, email: str, password: str, is_active: bool) -> UserType:
        try:
            user = User(id=UserId, username=username, email=email, password_hashed=get_password_hash(password), is_active=is_active)
            with Session(engine) as session:
                session.add(user)
                session.commit()
                session.refresh(user)
                return user
        except Exception as e:
            print(e)
            raise HTTPException(status_code=404, detail="User not created")

    @strawberry.field
    async def update_user(self, userId: int, username: str, password: str, is_active: bool) -> UserType:
        try:
            with Session(engine) as session:
                stored_user = session.get(User, userId)
                new_data = {"username": username, "password": password, "is_active": is_active}
                updated_user = stored_user.model_copy(update=new_data)
                session.add(updated_user)
                session.commit()
                session.refresh(updated_user)
            return updated_user
        except Exception as e:
            raise HTTPException(status_code=404, detail="User not found")
    
    @strawberry.field
    async def delete_user(self, userId: int) -> UserType:
        try:
            with Session(engine) as session:
                user = session.get(User, userId)
                if not user:
                    raise HTTPException(status_code=404, detail="User not found")
                session.delete(user)        
                session.commit()
            return user
        except Exception as e:
            raise HTTPException(status_code=404, detail="User not found")

    
    @strawberry.field
    async def login_for_access_token(self, email: str, password: str ) -> TokenType:
        with Session(engine) as session:
            user = authenticate_user(session, email=email, password=password)
        if not user:
            raise HTTPException(
                status_code=401,
                detail="Incorrect email or password",
                headers={"WWW-Authenticate": "Bearer"},
            )
        access_token_expires = timedelta(minutes=15)
        access_token = create_access_token(
            data={"sub": user.email}, expires_delta=access_token_expires
        )
        return  TokenType(access_token=access_token, token_type="bearer")
    




schema = strawberry.Schema(query=Query, mutation=Mutation)

