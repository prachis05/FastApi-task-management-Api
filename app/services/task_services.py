from sqlalchemy.orm import Session

from app import models
from app.schemas import Request, TaskUpdate


def createTask (db : Session,item : Request):
    task = models.Task ( 
    **item.model_dump(),
    status = False )

    db.add(task)
    db.commit()

    return task


def getAllTasks(db : Session):
    task = db.query(models.Task).all()
    return task 


def getTaskById(db : Session,id : int):
    task = db.query(models.Task).filter(models.Task.id==id).first()
    return task


def updateTask(db : Session,id : int, item : TaskUpdate):
    task = getTaskById(db,id)
    if task is None:
        return None
    
    task.title = item.title
    task.description = item.description
    task.status = item.status
    db.commit()
    return task


def deleteTask(db : Session,id : int):
    task = getTaskById(db,id)
    if task is None:
        return None

    db.delete(task)
    db.commit()
    return task


def completeTask(db : Session,id : int):
    task = getTaskById(db,id)
    if task is None:
        return None

    task.status= True
    db.commit()
    return task

    
    











