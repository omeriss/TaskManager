from abc import ABC, abstractmethod
from datetime import datetime
from typing import Optional, List
from app.domain.entities.task import Task, TaskStatus


class ITaskRepository(ABC):
    """Interface for Task Repository"""

    @abstractmethod
    def create_task(self, task: Task) -> Task:
        """
        Create a new task
        :param task: the task to create
        :return: created task
        """
        pass

    @abstractmethod
    def get_task(self, task_id: int) -> Optional[Task]:
        """
        Get a task by its ID
        :param task_id: the ID of the task
        :return: the task if found, else None
        """
        pass

    @abstractmethod
    def edit_task(self, task: Task) -> Task | None:
        """
        Edit an existing task
        :param task: the task with updated information
        :return: the updated task if successful, None if the task does not exist
        """
        pass

    @abstractmethod
    def delete_task(self, task_id: int) -> bool:
        """
        Delete a task by its ID
        :param task_id: the task ID to delete
        :return: True if deletion was successful, False if task does not exist
        """
        pass

    @abstractmethod
    def get_tasks(self, from_date: Optional[datetime] = None, to_date: Optional[datetime] = None,
                  status: Optional[TaskStatus] = None, title_contains: Optional[str] = None) -> List[Task]:
        """
        Get tasks filtered by date range and status
        :param from_date: the start date for filtering
        :param to_date: the end date for filtering
        :param status: the status to filter tasks
        :param title_contains: string that should be contained in the task title
        :return: list of tasks matching
        """
        pass

