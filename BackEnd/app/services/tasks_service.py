from datetime import datetime
from app.domain.repositories.task_repository import ITaskRepository
from app.domain.entities.task import Task


class TasksService:
    def __init__(self, task_repository: ITaskRepository):
        self.task_repository = task_repository

    def create_task(self, title: str, description: str | None) -> Task:
        task = Task(title=title, description=description, task_id=None, created_at=datetime.now())

        return self.task_repository.create_task(task)

    def get_task(self, task_id: int) -> Task | None:
        return self.task_repository.get_task(task_id)

    def complete_task(self, task_id: int) -> Task:
        task = self.task_repository.get_task(task_id)
        task.set_completed()

        return self.task_repository.edit_task(task)

    def delete_task(self, task_id: int) -> bool:
        return self.task_repository.delete_task(task_id)

    def get_tasks(self, from_date: datetime | None = None, to_date: datetime | None = None,
                  status: str | None = None) -> list[Task]:
        return self.task_repository.get_tasks(from_date, to_date, status)

