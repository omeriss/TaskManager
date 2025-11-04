"""Unit tests for TasksService using a mock repository."""
import pytest
from datetime import datetime, timedelta
from app.services.tasks_service import TasksService
from app.domain.entities.task import Task, TaskStatus
from tests.mock_task_repository import MockTaskRepository

# Note if someone reads this: Those tests are kind of pointless because there is not much logic in this app, I did them
# just to show that I know how to write tests


class TestTasksService:
    """Test suite for TasksService"""

    @pytest.fixture
    def mock_repo(self):
        """Fixture to provide a fresh mock repository for each test"""
        return MockTaskRepository()

    @pytest.fixture
    def service(self, mock_repo):
        """Fixture to provide a TasksService with a mock repository"""
        return TasksService(mock_repo)

    def test_create_task_success(self, service, mock_repo):
        """Test creating a task successfully"""
        title = "Test Task"
        description = "Test Description"
        due_date = datetime.now() + timedelta(days=1)

        task = service.create_task(title, description, due_date)

        assert task is not None
        assert task.id is not None
        assert task.id > 0
        assert task.title == title
        assert task.description == description
        assert task.due_date == due_date
        assert task.status == TaskStatus.PENDING
        assert task.completed_at is None
        assert len(mock_repo.tasks) == 1

    def test_create_task_without_description(self, service, mock_repo):
        """Test creating a task without a description"""
        title = "Task without description"
        due_date = datetime.now() + timedelta(days=2)

        task = service.create_task(title, None, due_date)

        assert task is not None
        assert task.title == title
        assert task.description is None
        assert len(mock_repo.tasks) == 1

    def test_get_task_success(self, service, mock_repo):
        """Test getting an existing task"""
        created_task = service.create_task("Test Task", "Description", datetime.now())

        retrieved_task = service.get_task(created_task.id)

        assert retrieved_task is not None
        assert retrieved_task.id == created_task.id
        assert retrieved_task.title == created_task.title
        assert retrieved_task.description == created_task.description

    def test_get_task_not_found(self, service):
        """Test getting a non-existent task"""
        task = service.get_task(123)

        assert task is None

    def test_complete_task_success(self, service, mock_repo):
        """Test completing a task"""
        task = service.create_task("Task to complete", "Description", datetime.now())
        assert task.status == TaskStatus.PENDING
        assert task.completed_at is None

        completed_task = service.complete_task(task.id)

        assert completed_task is not None
        assert completed_task.id == task.id
        assert completed_task.status == TaskStatus.COMPLETED
        assert completed_task.completed_at is not None

    def test_complete_task_sets_timestamp(self, service):
        """Test that completing a task sets the completed_at timestamp."""
        task = service.create_task("Task", "Desc", datetime.now())
        before_completion = datetime.now()

        completed_task = service.complete_task(task.id)
        after_completion = datetime.now()

        assert completed_task.completed_at >= before_completion
        assert completed_task.completed_at <= after_completion

    def test_complete_task_twice_keeps_original_timestamp(self, service):
        """Test that completing a task twice does not update the completed_at timestamp the second time"""
        task = service.create_task("Task", "Desc", datetime.now())

        completed_task_first = service.complete_task(task.id)
        first_completed_at = completed_task_first.completed_at

        assert completed_task_first.status == TaskStatus.COMPLETED
        assert first_completed_at is not None

        # Wait a tiny bit to ensure timestamps would be different if updated
        import time
        time.sleep(0.01)

        # Complete the task for the second time
        completed_task_second = service.complete_task(task.id)
        second_completed_at = completed_task_second.completed_at

        # The completed_at timestamp should remain the same
        assert completed_task_second.status == TaskStatus.COMPLETED
        assert second_completed_at == first_completed_at

    def test_delete_task_success(self, service, mock_repo):
        """Test deleting an existing task"""
        task = service.create_task("Task to delete", "Description", datetime.now())
        assert len(mock_repo.tasks) == 1

        result = service.delete_task(task.id)

        assert result is True
        assert len(mock_repo.tasks) == 0

        deleted_task = service.get_task(task.id)
        assert deleted_task is None

    def test_delete_task_not_found(self, service):
        """Test deleting a non-existent task"""
        result = service.delete_task(123)

        assert result is False

    def test_get_tasks_empty(self, service):
        """Test getting tasks when repository is empty"""
        tasks = service.get_tasks()

        assert tasks == []
        assert len(tasks) == 0

    def test_get_tasks_all(self, service):
        """Test getting all tasks without filters."""
        task1 = service.create_task("Task 1", "Desc 1", datetime.now())
        task2 = service.create_task("Task 2", "Desc 2", datetime.now())
        task3 = service.create_task("Task 3", "Desc 3", datetime.now())

        tasks = service.get_tasks()

        assert len(tasks) == 3
        assert task1 in tasks
        assert task2 in tasks
        assert task3 in tasks

    def test_get_tasks_xlsx_empty(self, service):
        """Test generating XLSX for empty task list."""
        xlsx_data = service.get_tasks_xlsx()

        assert xlsx_data is not None
        assert isinstance(xlsx_data, bytes)
        assert len(xlsx_data) > 0

    def test_get_tasks_xlsx_with_tasks(self, service):
        """Test generating XLSX with tasks."""
        due_date = datetime.now() + timedelta(days=1)
        task1 = service.create_task("Task 1", "Description 1", due_date)
        task2 = service.create_task("Task 2", "Description 2", due_date)
        service.complete_task(task2.id)

        xlsx_data = service.get_tasks_xlsx()

        assert xlsx_data is not None
        assert isinstance(xlsx_data, bytes)
        assert len(xlsx_data) > 0

    def test_get_tasks_xlsx_with_none_values(self, service):
        """Test generating XLSX with tasks that have None values."""
        task1 = service.create_task("Task without description", None, None)

        xlsx_data = service.get_tasks_xlsx()

        assert xlsx_data is not None
        assert isinstance(xlsx_data, bytes)
        assert len(xlsx_data) > 0
