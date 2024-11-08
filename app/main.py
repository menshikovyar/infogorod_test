from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from . import models, schemas, crud
from .db import engine, SessionLocal
from .celery_worker import background_task
from celery.result import AsyncResult
import uvicorn

models.Base.metadata.create_all(bind = engine)

app = FastAPI()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close() 

@app.get("/")
async def read_root():
    return {"message": "Привет, это мое FastAPI приложение!"}

@app.post("/tasks/", response_model = schemas.Task)
def create_task(task: schemas.TaskCreate, db: Session = Depends(get_db)):
    db_task = crud.create_task(db, task)
    background_task.delay(db_task.id, db_task.title)
    return db_task

@app.get("/tasks/", response_model = list[schemas.Task])
def read_tasks(db: Session = Depends(get_db)):
    return crud.get_tasks(db)

@app.get("/tasks/{task_id}", response_model = schemas.Task)
def read_task(task_id: int, db: Session = Depends(get_db)):
    db_task = crud.get_task(db, task_id)
    if db_task is None:
        raise HTTPException(status_code = 404, detail = "Задача не найдена!")
    return db_task

@app.put("/tasks/{task_id}", response_model = schemas.Task)
def update_task(task_id: int, task: schemas.TaskCreate, db: Session = Depends(get_db)):
    db_task = crud.update_task(db, task_id, task)
    return db_task

@app.delete("/tasks/{task_id}", response_model = schemas.Task)
def delete_task(task_id: int, db: Session = Depends(get_db)):
    db_task = crud.delete_task(db, task_id)
    return None


if __name__ == "__main__":
  uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)