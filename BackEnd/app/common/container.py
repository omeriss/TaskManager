from dependency_injector import containers, providers
from app.infrastructure.database.session import get_session
from app.infrastructure.database.task_repository_database import TaskRepositoryDatabase
from app.services.tasks_service import TasksService


class Container(containers.DeclarativeContainer):
    """Dependency injection container with the dependency-injector library."""

    # Database session
    db_session = providers.Resource(
        get_session
    )

    # Repository
    task_repository = providers.Factory(
        TaskRepositoryDatabase,
        session=db_session
    )

    # Services
    tasks_service = providers.Factory(
        TasksService,
        task_repository=task_repository
    )


