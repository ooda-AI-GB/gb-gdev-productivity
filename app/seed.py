from datetime import date, timedelta

from sqlalchemy.orm import Session

from app.models import Comment, Label, Milestone, Project, Task, TimeEntry


def seed_database(db: Session) -> None:
    """Populate the database with sample data. No-ops if data already exists."""
    if db.query(Project).count() > 0:
        return

    today = date.today()

    # ── Projects ─────────────────────────────────────────────────────────────
    p1 = Project(
        name="Website Redesign",
        description="Complete overhaul of the company website with a modern, responsive design and improved UX.",
        status="active",
        owner="alice@company.com",
        start_date=today - timedelta(days=30),
        target_date=today + timedelta(days=60),
        priority="high",
        tags=["web", "design", "frontend"],
    )
    p2 = Project(
        name="Mobile App Launch",
        description="Launch the company mobile app on iOS and Android with payments and push notifications.",
        status="active",
        owner="bob@company.com",
        start_date=today - timedelta(days=60),
        target_date=today + timedelta(days=30),
        priority="critical",
        tags=["mobile", "ios", "android"],
    )
    p3 = Project(
        name="API Integration",
        description="Integrate third-party APIs for analytics, payment processing, and CRM sync.",
        status="paused",
        owner="charlie@company.com",
        start_date=today - timedelta(days=45),
        target_date=today + timedelta(days=45),
        priority="medium",
        tags=["api", "backend", "integration"],
    )
    p4 = Project(
        name="Internal Tooling",
        description="Build internal productivity tools including a time tracker and reporting dashboard.",
        status="completed",
        owner="alice@company.com",
        start_date=today - timedelta(days=120),
        target_date=today - timedelta(days=30),
        completed_date=today - timedelta(days=35),
        priority="low",
        tags=["internal", "tools"],
    )
    db.add_all([p1, p2, p3, p4])
    db.flush()

    # ── Tasks ─────────────────────────────────────────────────────────────────
    t1 = Task(
        project_id=p1.id,
        title="Design wireframes for all pages",
        description="Create detailed wireframes for homepage, about, services, and contact pages.",
        status="done",
        priority="high",
        assignee="alice@company.com",
        due_date=today - timedelta(days=20),
        completed_date=today - timedelta(days=22),
        estimated_hours=16.0,
        actual_hours=14.5,
        tags=["design", "wireframes"],
    )
    t2 = Task(
        project_id=p1.id,
        title="Implement homepage",
        description="Build the new homepage: hero section, feature grid, testimonials, and footer.",
        status="in_progress",
        priority="high",
        assignee="dave@company.com",
        due_date=today + timedelta(days=7),
        estimated_hours=24.0,
        actual_hours=12.0,
        tags=["frontend", "html", "css"],
    )
    t3 = Task(
        project_id=p1.id,
        title="Write marketing copy",
        description="Write compelling copy for all pages aligned with the new brand voice.",
        status="todo",
        priority="medium",
        assignee="eve@company.com",
        due_date=today + timedelta(days=14),
        estimated_hours=8.0,
        tags=["content", "copywriting"],
    )
    t4 = Task(
        project_id=p1.id,
        title="SEO optimisation",
        description="Implement on-page SEO: meta tags, structured data, sitemap, and page speed.",
        status="todo",
        priority="low",
        assignee="frank@company.com",
        due_date=today + timedelta(days=45),
        estimated_hours=12.0,
        tags=["seo", "marketing"],
    )
    t5 = Task(
        project_id=p2.id,
        title="User authentication",
        description="Implement registration, login, password reset, and OAuth (Google, Apple).",
        status="in_progress",
        priority="critical",
        assignee="bob@company.com",
        due_date=today + timedelta(days=5),
        estimated_hours=32.0,
        actual_hours=22.0,
        tags=["auth", "security"],
    )
    t6 = Task(
        project_id=p2.id,
        title="Payment integration",
        description="Integrate Stripe for subscriptions and one-time purchases; handle webhooks.",
        status="blocked",
        priority="high",
        assignee="charlie@company.com",
        due_date=today + timedelta(days=14),
        estimated_hours=20.0,
        tags=["payments", "stripe"],
    )
    t7 = Task(
        project_id=p2.id,
        title="Push notifications",
        description="Set up FCM for Android and APNs for iOS; implement notification preferences.",
        status="todo",
        priority="medium",
        assignee="dave@company.com",
        due_date=today + timedelta(days=21),
        estimated_hours=16.0,
        tags=["notifications", "mobile"],
    )
    t8 = Task(
        project_id=p3.id,
        title="Update API documentation",
        description="Sync OpenAPI spec with the latest endpoint changes and add usage examples.",
        status="review",
        priority="low",
        assignee="alice@company.com",
        due_date=today - timedelta(days=2),   # deliberately overdue
        estimated_hours=4.0,
        actual_hours=3.0,
        tags=["docs", "api"],
    )
    t9 = Task(
        project_id=None,
        title="Weekly team sync",
        description="Prepare agenda, run the weekly all-hands, and distribute meeting notes.",
        status="todo",
        priority="medium",
        due_date=today + timedelta(days=2),
        estimated_hours=1.0,
        tags=["meeting", "recurring"],
    )
    t10 = Task(
        project_id=p2.id,
        title="App Store listing preparation",
        description="Write store descriptions, prepare screenshots, and submit for review.",
        status="todo",
        priority="high",
        assignee="eve@company.com",
        due_date=today + timedelta(days=25),
        estimated_hours=6.0,
        tags=["app-store", "marketing"],
    )
    db.add_all([t1, t2, t3, t4, t5, t6, t7, t8, t9, t10])
    db.flush()

    # Subtask (child of t5)
    t5_sub = Task(
        project_id=p2.id,
        title="Implement JWT token service",
        description="Build token generation, validation, refresh, and revocation logic.",
        status="done",
        priority="critical",
        assignee="bob@company.com",
        due_date=today - timedelta(days=5),
        completed_date=today - timedelta(days=6),
        estimated_hours=8.0,
        actual_hours=7.0,
        parent_task_id=t5.id,
        tags=["jwt", "security"],
    )
    db.add(t5_sub)
    db.flush()

    # ── Comments ──────────────────────────────────────────────────────────────
    db.add_all([
        Comment(
            task_id=t1.id,
            author="alice@company.com",
            content="Wireframes approved by the client after two rounds of feedback. "
                    "Moving straight to implementation.",
        ),
        Comment(
            task_id=t1.id,
            author="dave@company.com",
            content="Thanks! Starting on the homepage today. Will share a live preview by Friday.",
        ),
        Comment(
            task_id=t2.id,
            author="bob@company.com",
            content="Hero section looks great. Could we try a darker background variant too?",
        ),
        Comment(
            task_id=t2.id,
            author="dave@company.com",
            content="Dark variant added to the Figma file — link in the project channel.",
        ),
        Comment(
            task_id=t5.id,
            author="bob@company.com",
            content="Auth module is 70% complete. JWT + basic email login working end-to-end. "
                    "OAuth is next.",
        ),
        Comment(
            task_id=t6.id,
            author="charlie@company.com",
            content="Blocked on Stripe API keys — waiting for finance team approval. "
                    "ETA is end of this week.",
        ),
        Comment(
            task_id=t8.id,
            author="alice@company.com",
            content="Draft docs ready for review. Added examples for all new endpoints.",
        ),
    ])

    # ── Labels ────────────────────────────────────────────────────────────────
    db.add_all([
        Label(name="bug",           color="#e74c3c", description="Something isn't working"),
        Label(name="feature",       color="#2ecc71", description="New feature or request"),
        Label(name="documentation", color="#3498db", description="Improvements or additions to docs"),
        Label(name="urgent",        color="#e67e22", description="Needs immediate attention"),
        Label(name="design",        color="#9b59b6", description="Design-related tasks"),
        Label(name="backend",       color="#1abc9c", description="Server-side / backend work"),
        Label(name="frontend",      color="#f39c12", description="Client-side / frontend work"),
        Label(name="blocked",       color="#c0392b", description="Blocked on an external dependency"),
    ])

    # ── Time Entries ──────────────────────────────────────────────────────────
    db.add_all([
        TimeEntry(task_id=t1.id, user="alice@company.com", hours=8.0,
                  date=today - timedelta(days=25),
                  description="Initial wireframe design — all pages drafted"),
        TimeEntry(task_id=t1.id, user="alice@company.com", hours=6.5,
                  date=today - timedelta(days=24),
                  description="Revisions based on stakeholder feedback"),
        TimeEntry(task_id=t2.id, user="dave@company.com", hours=4.0,
                  date=today - timedelta(days=1),
                  description="Project setup, CSS framework, and base layout"),
        TimeEntry(task_id=t2.id, user="dave@company.com", hours=3.5,
                  date=today,
                  description="Hero section and top navigation"),
        TimeEntry(task_id=t5.id, user="bob@company.com", hours=6.0,
                  date=today - timedelta(days=1),
                  description="Auth middleware and session management"),
        TimeEntry(task_id=t5.id, user="bob@company.com", hours=4.5,
                  date=today,
                  description="OAuth Google flow — end-to-end test passing"),
        TimeEntry(task_id=t5_sub.id, user="bob@company.com", hours=7.0,
                  date=today - timedelta(days=6),
                  description="JWT generation, validation, refresh, and revocation"),
        TimeEntry(task_id=t8.id, user="alice@company.com", hours=3.0,
                  date=today - timedelta(days=3),
                  description="Rewrote endpoint docs with request/response examples"),
    ])

    # ── Milestones ────────────────────────────────────────────────────────────
    db.add_all([
        Milestone(
            project_id=p1.id,
            title="Design Phase Complete",
            description="All wireframes and high-fidelity designs approved by stakeholders.",
            due_date=today - timedelta(days=20),
            status="reached",
        ),
        Milestone(
            project_id=p1.id,
            title="Beta Launch",
            description="Website ready for beta user testing with core pages live.",
            due_date=today + timedelta(days=30),
            status="pending",
        ),
        Milestone(
            project_id=p1.id,
            title="Public Launch",
            description="Full public launch with SEO, analytics, and content complete.",
            due_date=today + timedelta(days=60),
            status="pending",
        ),
        Milestone(
            project_id=p2.id,
            title="Alpha Release",
            description="Internal dog-food release for the core team.",
            due_date=today - timedelta(days=15),
            status="reached",
        ),
        Milestone(
            project_id=p2.id,
            title="Beta Release",
            description="Closed beta for 500 early-access users.",
            due_date=today + timedelta(days=30),
            status="pending",
        ),
        Milestone(
            project_id=p2.id,
            title="App Store Submission",
            description="Submit to App Store and Google Play for review.",
            due_date=today + timedelta(days=55),
            status="pending",
        ),
        Milestone(
            project_id=p3.id,
            title="API Integration MVP",
            description="Core third-party integrations functional in staging.",
            due_date=today - timedelta(days=10),
            status="missed",
        ),
    ])

    db.commit()
    print("Database seeded with sample data.")
