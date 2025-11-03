from typing import Optional
from datetime import datetime
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
    tasks_service: TasksService = Depends(Provide[Container.tasks_service])
):
    """
    Create a new task
    :param request: the create params
    :param tasks_service: injected tasks service
    :return: the created task
    """
    created_task = tasks_service.create_task(
        title=request.title,
        description=request.description
    )

    return created_task


@router.get("")
@inject
async def get_tasks(
    from_date: Optional[datetime] = None,
    to_date: Optional[datetime] = None,
    status: Optional[TaskStatus] = None,
    tasks_service: TasksService = Depends(Provide[Container.tasks_service])
):
    """
    Get tasks with optional filters
    :param from_date: the start date filter
    :param to_date: the end date filter
    :param status: the status filter
    :param tasks_service: injected tasks service
    :return: list of tasks
    """
    tasks = tasks_service.get_tasks(from_date=from_date, to_date=to_date, status=status)

    return tasks


@router.get("/summary")
@inject
def export_task_summary(
        tasks_service: TasksService = Depends(Provide[Container.tasks_service])
):
    """
    Export a summary of tasks
    :param tasks_service: injected tasks service
    :return: task summary in xlsx format
    """
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
    tasks_service: TasksService = Depends(Provide[Container.tasks_service])
):
    """
    Get a task by its ID
    :param task_id: the ID of the task
    :param tasks_service: injected tasks service
    :return: the task
    """
    task = tasks_service.get_task(task_id)

    return task


@router.delete("/{task_id}")
@inject
async def delete_task(
    task_id: int,
    tasks_service: TasksService = Depends(Provide[Container.tasks_service])
):
    """
    Delete a task by its ID
    :param task_id: the ID of the task
    :param tasks_service: the injected tasks service
    :return:
    """
    tasks_service.delete_task(task_id)

    return {"message": "Task deleted successfully"}


@router.patch("/{task_id}/complete")
@inject
async def complete_task(
    task_id: int,
    tasks_service: TasksService = Depends(Provide[Container.tasks_service])
):
    """
    Mark a task as completed
    :param task_id: the ID of the task
    :param tasks_service: injected tasks service
    :return:
    """
    tasks_service.complete_task(task_id)

    return {"message": "Task marked as completed"}
