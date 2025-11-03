from datetime import datetime
import enum


class TaskStatus(str, enum.Enum):
    """enum representing the status of a Task"""

    PENDING = "pending"
    COMPLETED = "completed"


class Task:
    """entity representing a Task object"""

    id: int
    title: str
    description: str | None = None
    status: TaskStatus = TaskStatus.PENDING
    due_date: datetime | None = None
    completed_at: datetime | None = None
    created_at: datetime

    def __init__(
        self,
        task_id: int | None,
        title: str,
        description: str | None,
        created_at: datetime,
        status: TaskStatus = TaskStatus.PENDING,
        due_date: datetime | None = None,
        completed_at: datetime | None = None,
    ):
        self.id = task_id if task_id is not None else -1
        self.title = title
        self.description = description
        self.status = status
        self.due_date = due_date
        self.completed_at = completed_at
        self.created_at = created_at

    def set_completed(self):
        self.status = TaskStatus.COMPLETED
        self.completed_at = datetime.now()

