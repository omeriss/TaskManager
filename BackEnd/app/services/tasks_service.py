from datetime import datetime
from app.domain.repositories.task_repository import ITaskRepository
from app.domain.entities.task import Task
from openpyxl import Workbook
from io import BytesIO
from typing import Optional


class TasksService:
    def __init__(self, task_repository: ITaskRepository):
        self.task_repository = task_repository

    def create_task(self, title: str, description: Optional[str], due_date: Optional[datetime]) -> Task:
        """
        Create a new task
        :param title: title of the task
        :param description: the description of the task
        :param due_date: the due date of the task
        :return: The created task
        """
        task = Task(title=title, description=description, task_id=None, due_date=due_date, created_at=datetime.now())

        return self.task_repository.create_task(task)

    def get_task(self, task_id: int) -> Task | None:
        """
        Get a task by its ID
        :param task_id: ID of the task
        :return: The task or None if not found
        """
        return self.task_repository.get_task(task_id)

    def complete_task(self, task_id: int) -> Task:
        """
        Mark a task as completed
        :param task_id: ID of the task
        :return: The updated task
        """
        task = self.task_repository.get_task(task_id)
        task.set_completed()

        return self.task_repository.edit_task(task)

    def delete_task(self, task_id: int) -> bool:
        """
        Delete a task by its ID
        :param task_id: ID of the task
        :return: True if the task was deleted, False otherwise
        """
        return self.task_repository.delete_task(task_id)

    def get_tasks(self, from_date: Optional[datetime] = None, to_date: Optional[datetime] = None,
                  status: Optional[str] = None, title_contains: Optional[str] = None) -> list[Task]:
        """
        Get tasks with optional filters
        :param from_date: from create date to fileter
        :param to_date: to create date to filter
        :param status: status to filterj
        :param title_contains: title substring to filter
        :return: List of tasks
        """
        return self.task_repository.get_tasks(from_date, to_date, status, title_contains)

    def get_tasks_xlsx(self) -> bytes:
        """
        Export tasks to an xlsx file
        :return: Bytes of the xlsx file
        """
        tasks = self.task_repository.get_tasks()

        # create the xlsx file
        workbook = Workbook()
        sheet = workbook.active
        sheet.title = "Tasks"

        headers = ["Title", "Description", "Status", "Due Date", "Completed At", "Created At"]
        sheet.append(headers)

        for task in tasks:
            sheet.append([
                task.title,
                task.description or "",
                task.status.value,
                task.due_date.strftime("%Y-%m-%d %H:%M:%S") if task.due_date else "",
                task.completed_at.strftime("%Y-%m-%d %H:%M:%S") if task.completed_at else "",
                task.created_at.strftime("%Y-%m-%d %H:%M:%S"),
            ])

        # save the file to a bytes buffer
        output = BytesIO()
        workbook.save(output)
        output.seek(0)
        return output.getvalue()


