from typing import Optional
from datetime import datetime
from logging import Logger
from fastapi import APIRouter, Depends
from fastapi.responses import Response
from dependency_injector.wiring import inject, Provide
from app.api.schemas.requests.create_task_request import CreateTaskRequest
from app.domain.entities.task import TaskStatus
from app.services.tasks_service import TasksService
from app.common.container import Container


router = APIRouter()


@router.post("")
@inject
async def create_task(
    request: CreateTaskRequest,
    tasks_service: TasksService = Depends(Provide[Container.tasks_service]),
    logger: Logger = Depends(Provide[Container.logger])
):
    """
    Create a new task
    :param request: the create params
    :param tasks_service: injected tasks service
    :param logger: injected logger
    :return: the created task
    """
    logger.info(f"Creating task with title: {request.title}")

    created_task = tasks_service.create_task(
        title=request.title,
        description=request.description,
        due_date=request.due_date
    )

    return created_task


@router.get("")
@inject
async def get_tasks(
    from_date: Optional[datetime] = None,
    to_date: Optional[datetime] = None,
    status: Optional[TaskStatus] = None,
    title_contains: Optional[str] = None,
    tasks_service: TasksService = Depends(Provide[Container.tasks_service]),
    logger: Logger = Depends(Provide[Container.logger])
):
    """
    Get tasks with optional filters
    :param from_date: the start date filter
    :param to_date: the end date filter
    :param status: the status filter
    :param tasks_service: injected tasks service
    :param title_contains: filter by title substring
    :param logger: injected logger
    :return: list of tasks
    """
    logger.info(f"Getting tasks with filters - from_date: {from_date}, to_date: {to_date}, status: {status}, title_contains: {title_contains}")

    tasks = tasks_service.get_tasks(from_date=from_date, to_date=to_date, status=status, title_contains=title_contains)

    return tasks


@router.get("/summary")
@inject
def export_task_summary(
        tasks_service: TasksService = Depends(Provide[Container.tasks_service]),
        logger: Logger = Depends(Provide[Container.logger])
):
    """
    Export a summary of tasks
    :param tasks_service: injected tasks service
    :param logger: injected logger
    :return: task summary in xlsx format
    """
    logger.info("Exporting task summary to XLSX")

    xlsx_data = tasks_service.get_tasks_xlsx()

    return Response(
        content=xlsx_data,
        headers={
            "Content-Disposition": "attachment; filename=tasks_summary.xlsx"
        }
    )


@router.get("/{task_id}")
@inject
async def get_task(
    task_id: int,
    tasks_service: TasksService = Depends(Provide[Container.tasks_service]),
    logger: Logger = Depends(Provide[Container.logger])
):
    """
    Get a task by its ID
    :param task_id: the ID of the task
    :param tasks_service: injected tasks service
    :param logger: injected logger
    :return: the task
    """
    logger.info(f"Getting task with ID: {task_id}")

    task = tasks_service.get_task(task_id)

    return task


@router.delete("/{task_id}")
@inject
async def delete_task(
    task_id: int,
    tasks_service: TasksService = Depends(Provide[Container.tasks_service]),
    logger: Logger = Depends(Provide[Container.logger])
):
    """
    Delete a task by its ID
    :param task_id: the ID of the task
    :param tasks_service: the injected tasks service
    :param logger: injected logger
    :return:
    """
    logger.info(f"Deleting task with ID: {task_id}")

    tasks_service.delete_task(task_id)

    return {"message": "Task deleted successfully"}


@router.patch("/{task_id}/complete")
@inject
async def complete_task(
    task_id: int,
    tasks_service: TasksService = Depends(Provide[Container.tasks_service]),
    logger: Logger = Depends(Provide[Container.logger])
):
    """
    Mark a task as completed
    :param task_id: the ID of the task
    :param tasks_service: injected tasks service
    :param logger: injected logger
    :return:
    """
    logger.info(f"Marking task with ID: {task_id} as completed")

    tasks_service.complete_task(task_id)

    return {"message": "Task marked as completed"}
