from sqlalchemy.orm import Session
from . import models, schemas

def create_task(db: Session, task: schemas.TaskCreate):
    db_task = models.Task(title = task.title, description = task.description)
    db.add(db_task)
    db.commit()
    db.refresh(db_task)
    return db_task

def get_tasks(db: Session):
    return db.query(models.Task).all()

def get_task(db: Session, task_id: int):
    return db.get(models.Task, task_id)

def update_task(db: Session, task_id: int, task: schemas.TaskUpdate):
    updated_task = db.query(models.Task).filter(models.Task.id == task_id).update(task.dict(exclude_unset = True), synchronize_session = False)
    db.commit()
    if updated_task:
        return db.query(models.Task).filter(models.Task.id == task_id).first()
    return None

def delete_task(db: Session, task_id: int):
    db_task = db.query(models.Task).filter(models.Task.id == task_id).first()
    if db_task:
        db.delete(db_task)
        db.commit()
    return db_task
