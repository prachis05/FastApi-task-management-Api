from datetime import datetime

from pydantic import BaseModel, ConfigDict


class Request(BaseModel):
    title : str
    description : str


class TaskUpdate(BaseModel):
    title: str
    description: str
    status: bool    

class Response(BaseModel):
    id : int 
    status : bool
    created_at : datetime
    title : str
    description : str
    model_config = ConfigDict(from_attributes=True)
