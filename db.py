from sqlmodel import SQLModel, create_engine
from models import Todo, User

db_url = "sqlite:///todos.db"
engine = create_engine(db_url, connect_args={"check_same_thread": False})
SQLModel.metadata.create_all(engine)