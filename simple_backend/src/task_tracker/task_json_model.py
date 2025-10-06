import requests
from abc_model import BaseHTTPClient
from task_model import Task, TaskUpdate
from typing import List, Dict


class TasksJsonbin(BaseHTTPClient):

    def __init__(self, api_key: str, bin_id: str):
        self.url = f"https://api.jsonbin.io/v3/b/{bin_id}"
        self.headers = {
            'Content-Type': 'application/json',
            'X-Master-Key': api_key,
            'X-Access-Key': api_key
        }

    def _write_data(self, data: List[Dict]):
        response = requests.put(self.url, json=data, headers=self.headers)
        response.raise_for_status()
        return 'Ok'

    def request(self) -> List[Dict]:
        response = requests.get(url=self.url, headers=self.headers)
        response.raise_for_status()
        return response.json()['record']

    def _search_task(self, task_id: str, tasks: List[Dict]) -> Dict:
        for dct in tasks:
            if task_id == dct.get("id"):
                return dct
        raise KeyError(f"Задача с task_id {task_id} не найдена")

    def get_all_tasks(self) -> List:
        return [Task(**dct) for dct in self.request()]

    def add(self, task: Task, solution_llm: str):
        tasks = self.request()
        if solution_llm is not None:
            task.solution_llm = solution_llm
        tasks.append(task.dict())
        self._write_data(tasks)
        return 'ok'

    def up_data(self, task_id: str, task: TaskUpdate, solution_llm: str):
        tasks = self.request()
        dct = self._search_task(task_id, tasks)
        dct_up = {key: value for key, value in task.__dict__.items() if value is not None}
        dct.update(dct_up)
        if solution_llm is not None:
            dct['solution_llm'] = solution_llm
        self._write_data(tasks)
        return 'ok'

    def delete(self, task_id: str):
        tasks = self.request()
        dct = self._search_task(task_id, tasks)
        tasks.pop(tasks.index(dct))
        self._write_data(tasks)
        return 'ok'
