import logging
from dependency_injector import containers, providers
from app.infrastructure.database.session import get_session
from app.infrastructure.database.task_repository_database import TaskRepositoryDatabase
from app.services.tasks_service import TasksService


def configure_logger(name: str) -> logging.Logger:
    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)

    handler = logging.StreamHandler()
    handler.setLevel(logging.INFO)
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    handler.setFormatter(formatter)

    logger.addHandler(handler)

    return logger


class Container(containers.DeclarativeContainer):
    """Dependency injection container with the dependency-injector library."""

    # Logger
    logger = providers.Singleton(
        configure_logger,
        name="TaskManager"
    )

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


