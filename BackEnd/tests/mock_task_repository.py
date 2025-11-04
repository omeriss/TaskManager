from datetime import datetime
from typing import Optional, List
from app.domain.repositories.task_repository import ITaskRepository
from app.domain.entities.task import Task, TaskStatus


class MockTaskRepository(ITaskRepository):
    """Mock Task Repository using a list to store tasks in memory"""

    def __init__(self):
        self.tasks: List[Task] = []
        self._next_id = 1

    def create_task(self, task: Task) -> Task:
        task.id = self._next_id
        self._next_id += 1
        self.tasks.append(task)

        return task

    def get_task(self, task_id: int) -> Optional[Task]:
        for task in self.tasks:
            if task.id == task_id:
                return task

        return None

    def edit_task(self, task: Task) -> Task | None:
        for i, existing_task in enumerate(self.tasks):
            if existing_task.id == task.id:
                self.tasks[i] = task
                return task

        return None

    def delete_task(self, task_id: int) -> bool:
        for i, task in enumerate(self.tasks):
            if task.id == task_id:
                self.tasks.pop(i)
                return True

        return False

    def get_tasks(self, from_date: Optional[datetime] = None, to_date: Optional[datetime] = None,
                  status: Optional[TaskStatus] = None, title_contains: Optional[str] = None) -> List[Task]:
        # no filter logic this is part of the actual repo
        return self.tasks
