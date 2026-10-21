from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database import getDb
from app.schemas import Request, Response, TaskUpdate
from app.services import task_services

router = APIRouter()


@router.post("/tasks",
             response_model=Response,
             status_code=status.HTTP_201_CREATED )
def create_Task(task:Request ,db: Session = Depends(getDb)):
    return task_services.createTask(db,task)

@router.get("/tasks",response_model= list[Response])
def get_all_tasks(db: Session = Depends(getDb)):
    return task_services.getAllTasks(db)



@router.get("/tasks/{task_id}",response_model=Response)
def get_task_by_id(task_id : int, db: Session = Depends(getDb)):
    task = task_services.getTaskById(db,task_id)
    if task is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found")

    return task

@router.put("/tasks/{task_id}",response_model=Response)
def update_task(task_id : int, taskdetail : TaskUpdate, db: Session = Depends(getDb)):
    updatedTask = task_services.updateTask(db,task_id,taskdetail)
    if updatedTask is None:
         raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found")

    return updatedTask  


@router.delete("/tasks/{task_id}",status_code=status.HTTP_204_NO_CONTENT)
def delete_task(task_id:int, db: Session = Depends(getDb)):
    deletedTask=task_services.deleteTask(db,task_id)
    if deletedTask is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found"
        )




@router.patch("/tasks/{task_id}/complete",response_model=Response)
def complete_task(task_id : int, db: Session = Depends(getDb)):
    completedTask = task_services.completeTask(db,task_id)
    if completedTask is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found"
            )

    return completedTask




