import json
import csv
from datetime import datetime
from typing import List, Optional
from func import read_csv, write_csv

class Task:
    def __init__(self, task_id: int, title: str, description: str, done: bool = False,
                 priority: str = 'cредний', due_date: Optional[str] = None):
        self.id = task_id
        self.title = title
        self.description = description
        self.done = done
        self.priority = priority
        self.due_date = due_date or datetime.now().strftime('%d.%m.%Y')

    def to_dict(self) -> dict:
        return {
            'id': self.id,
            'title': self.title,
            'description': self.description,
            'done': self.done,
            'priority': self.priority,
            'due_date': self.due_date,
        }

    @classmethod
    def from_dict(cls, data: dict):
        return cls(data['id'], data['title'], data['description'],
                   data['done'], data['priority'], data['due_date'])


class TaskManager:
    def __init__(self, storage_file: str = 'tasks.json'):
        self.storage_file = storage_file
        self.tasks: List[Task] = self.load_tasks()

    def load_tasks(self) -> List[Task]:
        try:
            with open(self.storage_file, 'r') as file:
                data = json.load(file)
                return [Task.from_dict(task) for task in data]
        except (FileNotFoundError, json.JSONDecodeError):
            return []

    def save_tasks(self):
        with open(self.storage_file, 'w') as file:
            json.dump([task.to_dict() for task in self.tasks], file, indent=4)

    def add_task(self, title: str, description: str, priority: str, due_date: str):
        task_id = max([task.id for task in self.tasks], default=0) + 1
        new_task = Task(task_id, title, description, False, priority, due_date)
        self.tasks.append(new_task)
        self.save_tasks()
        print(f'Задача "{title}" успешно добавлена')

    def list_tasks(self):
        if not self.tasks:
            print('Нет доступных задач')
        else:
            for task in self.tasks:
                status = 'Выполнена' if task.done else 'Не выполнена'
                print(f'ID: {task.id}, Title: {task.title}, Status: {status}, '
                      f'Priority: {task.priority}, Due Date: {task.due_date}')

    def mark_task_done(self, task_id: int):
        task = next((task for task in self.tasks if task.id == task_id), None)
        if task:
            task.done = True
            self.save_tasks()
            print(f'Задача с ID {task_id} отмечена как выполненная')
        else:
            print('Задача не найдена')

    def edit_task(self, task_id: int, new_title: str, new_description: str,
                  new_priority: str, new_due_date: str):
        task = next((task for task in self.tasks if task.id == task_id), None)
        if task:
            task.title = new_title
            task.description = new_description
            task.priority = new_priority
            task.due_date = new_due_date
            self.save_tasks()
            print(f'Задача с ID {task_id} успешно обновлена')
        else:
            print('Задача не найдена')

    def delete_task(self, task_id: int):
        self.tasks = [task for task in self.tasks if task.id != task_id]
        self.save_tasks()
        print(f'Задача с ID {task_id} успешно удалена')

    def export_to_csv(self, file_name):
        write_csv(file_name, [task.to_dict() for task in self.tasks], ['id', 'title', 'description', 'priority', 'done', 'due_date'])
        print(f'Задачи успешно экспортированы в {file_name}')

    def import_from_csv(self, file_name):
        data = read_csv(file_name)
        for row in data:
            self.add_task(row['title'], row['description'], row['priority'], row['due_date'])
        print(f'Задачи успешно импортированы из {file_name}')