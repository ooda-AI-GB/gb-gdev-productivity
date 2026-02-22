from datetime import date, datetime
from typing import Any, Dict, List, Optional

from pydantic import BaseModel, ConfigDict


# ── Enums (string literals used in Pydantic for validation) ─────────────────

class ProjectStatus:
    active = "active"
    paused = "paused"
    completed = "completed"
    archived = "archived"


class Priority:
    low = "low"
    medium = "medium"
    high = "high"
    critical = "critical"


class TaskStatus:
    todo = "todo"
    in_progress = "in_progress"
    review = "review"
    blocked = "blocked"
    done = "done"


class MilestoneStatus:
    pending = "pending"
    reached = "reached"
    missed = "missed"


# ── Project ──────────────────────────────────────────────────────────────────

class ProjectCreate(BaseModel):
    name: str
    description: Optional[str] = None
    status: str = "active"
    owner: Optional[str] = None
    start_date: Optional[date] = None
    target_date: Optional[date] = None
    completed_date: Optional[date] = None
    priority: str = "medium"
    tags: Optional[List[str]] = []


class ProjectUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    status: Optional[str] = None
    owner: Optional[str] = None
    start_date: Optional[date] = None
    target_date: Optional[date] = None
    completed_date: Optional[date] = None
    priority: Optional[str] = None
    tags: Optional[List[str]] = None


class ProjectResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    description: Optional[str]
    status: str
    owner: Optional[str]
    start_date: Optional[date]
    target_date: Optional[date]
    completed_date: Optional[date]
    priority: str
    tags: Optional[List[Any]]
    created_at: datetime
    updated_at: datetime


# ── Task ─────────────────────────────────────────────────────────────────────

class TaskCreate(BaseModel):
    title: str
    description: Optional[str] = None
    status: str = "todo"
    priority: str = "medium"
    assignee: Optional[str] = None
    due_date: Optional[date] = None
    completed_date: Optional[date] = None
    estimated_hours: Optional[float] = None
    actual_hours: Optional[float] = None
    tags: Optional[List[str]] = []
    project_id: Optional[int] = None
    parent_task_id: Optional[int] = None


class TaskUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    status: Optional[str] = None
    priority: Optional[str] = None
    assignee: Optional[str] = None
    due_date: Optional[date] = None
    completed_date: Optional[date] = None
    estimated_hours: Optional[float] = None
    actual_hours: Optional[float] = None
    tags: Optional[List[str]] = None
    project_id: Optional[int] = None
    parent_task_id: Optional[int] = None


class TaskResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    title: str
    description: Optional[str]
    status: str
    priority: str
    assignee: Optional[str]
    due_date: Optional[date]
    completed_date: Optional[date]
    estimated_hours: Optional[float]
    actual_hours: Optional[float]
    tags: Optional[List[Any]]
    project_id: Optional[int]
    parent_task_id: Optional[int]
    created_at: datetime
    updated_at: datetime


# ── Comment ──────────────────────────────────────────────────────────────────

class CommentCreate(BaseModel):
    author: Optional[str] = None
    content: str


class CommentUpdate(BaseModel):
    author: Optional[str] = None
    content: Optional[str] = None


class CommentResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    task_id: int
    author: Optional[str]
    content: str
    created_at: datetime


# ── Label ────────────────────────────────────────────────────────────────────

class LabelCreate(BaseModel):
    name: str
    color: Optional[str] = None
    description: Optional[str] = None


class LabelUpdate(BaseModel):
    name: Optional[str] = None
    color: Optional[str] = None
    description: Optional[str] = None


class LabelResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    color: Optional[str]
    description: Optional[str]


# ── TimeEntry ────────────────────────────────────────────────────────────────

class TimeEntryCreate(BaseModel):
    task_id: int
    user: Optional[str] = None
    hours: float
    date: date
    description: Optional[str] = None


class TimeEntryUpdate(BaseModel):
    user: Optional[str] = None
    hours: Optional[float] = None
    date: Optional[date] = None
    description: Optional[str] = None


class TimeEntryResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    task_id: int
    user: Optional[str]
    hours: float
    date: date
    description: Optional[str]
    created_at: datetime


# ── Milestone ────────────────────────────────────────────────────────────────

class MilestoneCreate(BaseModel):
    project_id: int
    title: str
    description: Optional[str] = None
    due_date: Optional[date] = None
    status: str = "pending"


class MilestoneUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    due_date: Optional[date] = None
    status: Optional[str] = None


class MilestoneResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    project_id: int
    title: str
    description: Optional[str]
    due_date: Optional[date]
    status: str
    created_at: datetime


# ── Dashboard ────────────────────────────────────────────────────────────────

class DashboardResponse(BaseModel):
    projects_by_status: Dict[str, int]
    tasks_by_status: Dict[str, int]
    overdue_count: int
    this_week_tasks: int
    hours_logged: float
