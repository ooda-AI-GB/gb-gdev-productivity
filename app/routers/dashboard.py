from datetime import date, timedelta

from fastapi import APIRouter, Depends
from sqlalchemy import func
from sqlalchemy.orm import Session

from app.auth import verify_token
from app.database import get_db
from app.models import Project, Task, TimeEntry
from app.schemas import DashboardResponse

router = APIRouter()


@router.get("/dashboard", response_model=DashboardResponse)
def get_dashboard(
    db: Session = Depends(get_db),
    _: str = Depends(verify_token),
):
    today = date.today()
    week_end = today + timedelta(days=7)

    # Projects grouped by status
    project_rows = (
        db.query(Project.status, func.count(Project.id))
        .group_by(Project.status)
        .all()
    )
    projects_by_status = {row[0]: row[1] for row in project_rows}

    # Tasks grouped by status
    task_rows = (
        db.query(Task.status, func.count(Task.id))
        .group_by(Task.status)
        .all()
    )
    tasks_by_status = {row[0]: row[1] for row in task_rows}

    # Overdue: past due date and not done
    overdue_count = (
        db.query(Task)
        .filter(Task.due_date < today, Task.status != "done")
        .count()
    )

    # Tasks due within the next 7 days (and not yet done)
    this_week_tasks = (
        db.query(Task)
        .filter(Task.due_date >= today, Task.due_date <= week_end, Task.status != "done")
        .count()
    )

    # Total hours logged across all time entries
    hours_result = db.query(func.sum(TimeEntry.hours)).scalar()
    hours_logged = float(hours_result) if hours_result else 0.0

    return DashboardResponse(
        projects_by_status=projects_by_status,
        tasks_by_status=tasks_by_status,
        overdue_count=overdue_count,
        this_week_tasks=this_week_tasks,
        hours_logged=hours_logged,
    )
