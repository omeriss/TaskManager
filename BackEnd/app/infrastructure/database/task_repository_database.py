from datetime import datetime
from typing import Optional, List
from sqlalchemy.orm import Session
from app.domain.repositories.task_repository import ITaskRepository
from app.domain.entities.task import Task as TaskEntity, TaskStatus as TaskStatus
from app.infrastructure.database import models


class TaskRepositoryDatabase(ITaskRepository):
    """
    Task repository implementation using a SQL database with SQLAlchemy ORM.
    """
    def __init__(self, session: Session):
        self.session = session

    def create_task(self, task: TaskEntity) -> TaskEntity:
        db_task = models.Task(
            title=task.title,
            description=task.description,
            status=task.status,
            due_date=task.due_date,
            completed_at=task.completed_at,
            created_at=task.created_at
        )

        self.session.add(db_task)
        self.session.commit()
        self.session.refresh(db_task)

        return self._orm_to_entity(db_task)

    def get_task(self, task_id: int) -> Optional[TaskEntity]:
        db_task = self.session.query(models.Task).filter(models.Task.id == task_id).first()

        if db_task is None:
            return None

        return self._orm_to_entity(db_task)

    def edit_task(self, task: TaskEntity) -> TaskEntity | None:
        db_task = self.session.query(models.Task).filter(models.Task.id == task.id).first()

        if db_task is None:
            return None

        db_task.title = task.title
        db_task.description = task.description
        db_task.status = task.status
        db_task.due_date = task.due_date
        db_task.completed_at = task.completed_at

        self.session.commit()
        self.session.refresh(db_task)

        return self._orm_to_entity(db_task)

    def delete_task(self, task_id: int) -> bool:
        db_task = self.session.query(models.Task).filter(models.Task.id == task_id).first()

        if db_task is None:
            return False

        self.session.delete(db_task)
        self.session.commit()

        return True

    def get_tasks(self, from_date: Optional[datetime] = None, to_date: Optional[datetime] = None,
                  status: Optional[TaskStatus] = None) -> List[TaskEntity]:
        query = self.session.query(models.Task)

        # Add the filters
        if from_date:
            query = query.filter(models.Task.created_at >= from_date)
        if to_date:
            query = query.filter(models.Task.created_at <= to_date)
        if status:
            query = query.filter(models.Task.status == status)

        db_tasks = query.all()

        return [self._orm_to_entity(db_task) for db_task in db_tasks]

    @staticmethod
    def _orm_to_entity(db_task: models.Task) -> TaskEntity:
        """
        Converts a Task ORM model to a Task entity.
        :param db_task: the task ORM model
        :return: the task entity
        """
        return TaskEntity(
            task_id=db_task.id,
            title=db_task.title,
            description=db_task.description,
            status=TaskStatus(db_task.status.value),
            due_date=db_task.due_date,
            completed_at=db_task.completed_at,
            created_at=db_task.created_at
        )
