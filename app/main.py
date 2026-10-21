from fastapi import FastAPI

from app import models
from app.database import engine
from app.routers.tasks import router as tasks

models.Base.metadata.create_all(bind=engine)
app = FastAPI()

@app.get("/")
def root():
    return {
        "message": "Task Management API is running"
    }


app.include_router(tasks)

