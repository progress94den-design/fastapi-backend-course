from fastapi import HTTPException, FastAPI, Depends
from rest_framework import status
from typing import Annotated
from task import Task, TaskAdd, TaskUpdate
from task_json import TasksJsonbin

app = FastAPI()

tasks = TasksJsonbin()


@app.get("/tasks")
def get_tasks():
    return tasks.get_all_tasks()


@app.post("/tasks")
def create_task(task: Annotated[TaskAdd, Depends()]):
    obj = Task(**task.dict())
    tasks.add(obj)
    return 'Ok'


@app.put("/tasks/{task_id}")
def update_task(task_id: str, task: Annotated[TaskUpdate, Depends()]):
    try:
        tasks.up_data(task_id, task)
        return 'Ok'
    except KeyError:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Задача с task_id {task_id} не найдена")


@app.delete("/tasks/{task_id}")
def delete_task(task_id: str):
    try:
        tasks.delete(task_id)
        return 'Ok'
    except KeyError:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Задача с ID {task_id} не найдена")
