from contextlib import asynccontextmanager

from fastapi import FastAPI, Depends
from fastapi.responses import HTMLResponse
from sqlalchemy.orm import Session
from sqlalchemy import func as sqlfunc

from app.database import Base, SessionLocal, engine, get_db
from app.models import Project, Task, Comment, Label, TimeEntry, Milestone
from app.routers import comments, dashboard, labels, milestones, projects, tasks, time_entries
from app.seed import seed_database


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Create all tables, then seed sample data if the DB is empty.
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    try:
        seed_database(db)
    finally:
        db.close()
    yield


app = FastAPI(
    title="Productivity Pro",
    description=(
        "A task and project management API for teams. "
        "All endpoints (except /health) require `Authorization: Bearer <GDEV_API_TOKEN>`."
    ),
    version="1.0.0",
    lifespan=lifespan,
)

from viv_auth import init_auth
init_auth(app, engine, Base, get_db, app_name="Productivity Pro")


@app.get("/", response_class=HTMLResponse, include_in_schema=False)
def root_dashboard(db: Session = Depends(get_db)):
    proj_count = db.query(sqlfunc.count(Project.id)).scalar() or 0
    task_count = db.query(sqlfunc.count(Task.id)).scalar() or 0
    todo = db.query(sqlfunc.count(Task.id)).filter(Task.status == "todo").scalar() or 0
    in_prog = db.query(sqlfunc.count(Task.id)).filter(Task.status == "in_progress").scalar() or 0
    done = db.query(sqlfunc.count(Task.id)).filter(Task.status == "done").scalar() or 0
    label_count = db.query(sqlfunc.count(Label.id)).scalar() or 0
    milestone_count = db.query(sqlfunc.count(Milestone.id)).scalar() or 0
    recent_tasks = db.query(Task).order_by(Task.created_at.desc()).limit(8).all()
    rows = ""
    status_colors = {"todo": "#f5a623", "in_progress": "#4f8ef7", "done": "#34c759", "blocked": "#e74c3c"}
    for t in recent_tasks:
        sc = status_colors.get(t.status, "#7f8c9b")
        proj_name = t.project.name if t.project else "—"
        rows += f'<tr><td>{t.title}</td><td>{proj_name}</td><td><span style="color:{sc};font-weight:600">{t.status}</span></td><td>{t.priority}</td><td>{t.assignee or "—"}</td></tr>'
    return f"""<!DOCTYPE html>
<html lang="en"><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width,initial-scale=1.0"><title>Productivity Pro</title>
<style>
:root{{--primary:#4f8ef7;--success:#34c759;--warning:#f5a623;--danger:#e74c3c;--bg:#1a1f36;--bg-light:#f5f7fa;--card:#fff;--text:#2c3e50;--muted:#7f8c9b;--border:#e1e5eb}}
*{{box-sizing:border-box;margin:0;padding:0}}
body{{font-family:system-ui,-apple-system,sans-serif;background:var(--bg-light);color:var(--text);display:flex;min-height:100vh}}
.sidebar{{width:240px;background:var(--bg);color:#fff;display:flex;flex-direction:column;flex-shrink:0}}
.logo{{padding:1.5rem;font-size:1.4rem;font-weight:700}}
.nav-links{{flex:1;padding:0 1rem}}
.nav-link{{display:block;padding:.75rem 1rem;color:#cbd5e1;text-decoration:none;border-radius:6px;margin-bottom:.25rem}}
.nav-link:hover,.nav-link.active{{background:rgba(255,255,255,.15);color:#fff}}
.main{{flex:1;padding:2rem;overflow-y:auto}}
h1{{font-size:1.8rem;margin-bottom:1.5rem}}
.cards{{display:grid;grid-template-columns:repeat(auto-fit,minmax(180px,1fr));gap:1rem;margin-bottom:2rem}}
.card{{background:var(--card);border-radius:10px;padding:1.5rem;border:1px solid var(--border)}}
.card .label{{font-size:.85rem;color:var(--muted);margin-bottom:.25rem}}
.card .value{{font-size:1.6rem;font-weight:700}}
.card .value.blue{{color:var(--primary)}} .card .value.green{{color:var(--success)}} .card .value.orange{{color:var(--warning)}} .card .value.red{{color:var(--danger)}}
table{{width:100%;border-collapse:collapse;background:var(--card);border-radius:10px;overflow:hidden;border:1px solid var(--border)}}
th,td{{padding:.75rem 1rem;text-align:left;border-bottom:1px solid var(--border)}}
th{{background:var(--bg);color:#fff;font-weight:600;font-size:.85rem;text-transform:uppercase;letter-spacing:.5px}}
tr:last-child td{{border-bottom:none}}
.section-title{{font-size:1.1rem;font-weight:600;margin-bottom:1rem}}
a.api-link{{display:inline-block;margin-top:1rem;padding:.5rem 1rem;background:var(--primary);color:#fff;border-radius:6px;text-decoration:none;font-size:.9rem}}
</style></head><body>
<div class="sidebar">
  <div class="logo">Productivity Pro</div>
  <div class="nav-links">
    <a href="/" class="nav-link active">Dashboard</a>
    <a href="/docs" class="nav-link">API Docs</a>
  </div>
</div>
<div class="main">
  <h1>Dashboard</h1>
  <div class="cards">
    <div class="card"><div class="label">Projects</div><div class="value blue">{proj_count}</div></div>
    <div class="card"><div class="label">Total Tasks</div><div class="value">{task_count}</div></div>
    <div class="card"><div class="label">To Do</div><div class="value orange">{todo}</div></div>
    <div class="card"><div class="label">In Progress</div><div class="value blue">{in_prog}</div></div>
    <div class="card"><div class="label">Done</div><div class="value green">{done}</div></div>
    <div class="card"><div class="label">Labels</div><div class="value">{label_count}</div></div>
    <div class="card"><div class="label">Milestones</div><div class="value">{milestone_count}</div></div>
  </div>
  <div class="section-title">Recent Tasks</div>
  <table><thead><tr><th>Title</th><th>Project</th><th>Status</th><th>Priority</th><th>Assignee</th></tr></thead><tbody>{rows if rows else '<tr><td colspan="5" style="text-align:center;color:var(--muted)">No tasks yet</td></tr>'}</tbody></table>
  <a href="/docs" class="api-link">API Documentation &rarr;</a>
</div></body></html>"""


@app.get("/health", tags=["Health"])
def health_check():
    """Liveness probe — no auth required."""
    return {"status": "ok"}


PREFIX = "/api/v1"

app.include_router(projects.router,     prefix=PREFIX, tags=["Projects"])
app.include_router(tasks.router,        prefix=PREFIX, tags=["Tasks"])
app.include_router(comments.router,     prefix=PREFIX, tags=["Comments"])
app.include_router(labels.router,       prefix=PREFIX, tags=["Labels"])
app.include_router(time_entries.router, prefix=PREFIX, tags=["Time Entries"])
app.include_router(milestones.router,   prefix=PREFIX, tags=["Milestones"])
app.include_router(dashboard.router,    prefix=PREFIX, tags=["Dashboard"])
