from fastapi import FastAPI
from app.routers.tasks import router as tasks
from app.database import engine
from app import models

models.Base.metadata.create_all(bind=engine)
app = FastAPI()

@app.get("/")
def root():
    return {
        "message": "Task Management API is running"
    }


app.include_router(tasks)

