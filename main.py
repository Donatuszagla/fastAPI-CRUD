from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from sqlmodel import SQLModel, Field, create_engine, select, Session
from typing import Optional
from users import router

app = FastAPI()
app.include_router(router)


class Todo(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    title: str = Field(..., max_length=100)
    description: str
    completed: bool
    priority: str

db_url = "sqlite:///todos.db"
engine = create_engine(db_url, connect_args={"check_same_thread": False})
SQLModel.metadata.create_all(engine)


@app.get("/todos", tags=["todos"])  
def get_todos():
    try:
        with Session(engine) as session:
            todos = session.exec(select(Todo)).all()
        return todos
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/todos/{todo_id}", tags=["todos"]) 
def get_todo(todo_id: int):
    try:
        with Session(engine) as session:
            todo = session.get(Todo, todo_id)
        return todo
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.post("/todos", tags=["todos"])
def create_todo(todo: Todo):
    try:
        with Session(engine) as session:
            session.add(todo)
            session.commit()
            session.refresh(todo)
        return todo
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.put("/todos/{todo_id}", tags=["todos"])
def update_todo(todo_id: int, todo: Todo):
    try:
        with Session(engine) as session:
            stored_todo = session.get(Todo, todo_id)
            new_data = todo.model_dump(exclude_unset=True)
            updated_todo = stored_todo.model_copy(update=new_data)
            session.add(updated_todo)
            session.commit()
            session.refresh(updated_todo)
        return updated_todo
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e)) 

@app.delete("/todos/{todo_id}", tags=["todos"])
def delete_todo(todo_id: int):
    try:
        with Session(engine) as session:
            todo = session.get(Todo, todo_id)
            session.delete(todo)
            session.commit()
        return {"message": "Todo deleted successfully"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)