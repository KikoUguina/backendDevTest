from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List
import uuid

app = FastAPI()

class TaskBase(BaseModel):
    title: str
    description: str

class Task(TaskBase):
    id: str

tasks: List[Task] = []

@app.get("/tasks", response_model=List[Task])
def get_tasks():
    return tasks

@app.post("/tasks", response_model=Task)
def create_task(task_data: TaskBase):
    new_task = Task(id=str(uuid.uuid4()), **task_data.dict())
    tasks.append(new_task)
    return new_task

@app.put("/tasks/{task_id}", response_model=Task)
def update_task(task_id: str, updated_data: TaskBase):
    for index, task in enumerate(tasks):
        if task.id == task_id:
            updated_task = Task(id=task_id, **updated_data.dict())
            tasks[index] = updated_task
            return updated_task
    raise HTTPException(status_code=404, detail="Task not found")