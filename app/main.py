from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.database import Base, SessionLocal, engine
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
