from fastapi import FastAPI
from pydantic import BaseModel
from typing import List

app = FastAPI()

class Task(BaseModel):
    title: str
    description: str

tasks: List[Task] = []

@app.get("/tasks", response_model=List[Task])
def get_tasks():
    return tasks
