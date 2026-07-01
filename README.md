# 💰 Finance Tracker API

A personal finance REST API built with a modern Python backend stack — designed to demonstrate production-ready patterns: async architecture, JWT authentication, background task processing, and test-driven development.

## Tech Stack

| Layer | Technology |
|-------|-----------|
| Framework | FastAPI (async) |
| Database | PostgreSQL + SQLAlchemy 2.0 (async) + Alembic |
| Auth | JWT (python-jose + passlib/bcrypt) |
| Task Queue | Celery + Redis |
| Containerization | Docker Compose |
| Testing | pytest + pytest-asyncio |

## Features

- ✅ User registration and login with JWT authentication
- ✅ Full CRUD for financial transactions (income & expenses)
- ✅ Each user sees only their own data
- ✅ Filter transactions by type and category
- ✅ Real-time balance summary (income vs expenses)
- ✅ Async monthly report generation via Celery
- ✅ Report status tracking by task ID
- ✅ Input validation via Pydantic schemas
- ✅ Database migrations via Alembic
- ✅ Auto-generated API docs (Swagger UI)
- ✅ Test suite with TDD approach

## Getting Started

### Prerequisites
- Docker & Docker Compose

### Run locally

```bash
git clone https://github.com/yourusername/finance-tracker-api.git
cd finance-tracker-api/finance_tracker
docker compose up --build
```

Run database migrations:

```bash
docker compose exec api alembic upgrade head
```

Then open: `http://localhost:8000/docs`

### Run tests

```bash
cd finance_tracker
pip install aiosqlite pytest-asyncio httpx
pytest tests/ -v
```

## API Endpoints

### Auth
| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/auth/register` | Register new user |
| POST | `/auth/login` | Login and receive JWT token |

### Transactions (🔒 JWT required)
| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/transactions/` | Create transaction |
| GET | `/transactions/` | List own transactions (with filters) |
| GET | `/transactions/summary` | Income vs expenses balance |
| GET | `/transactions/{id}` | Get single transaction |
| PATCH | `/transactions/{id}` | Update transaction |
| DELETE | `/transactions/{id}` | Delete transaction |
| POST | `/transactions/reports/monthly` | Generate monthly report (async) |
| GET | `/transactions/reports/monthly/{task_id}/status` | Check report status |

## Project Structure

finance_tracker/
├── app/
│   ├── api/
│   │   └── endpoints/
│   │       ├── auth.py           # Register & login
│   │       └── transactions.py   # CRUD + reports
│   ├── core/
│   │   ├── config.py             # Settings (pydantic-settings)
│   │   ├── dependencies.py       # JWT dependency injection
│   │   └── security.py           # Password hashing, token generation
│   ├── db/
│   │   └── database.py           # Async engine & session
│   ├── models/
│   │   ├── user.py               # User model
│   │   └── transaction.py        # Transaction model
│   ├── schemas/
│   │   ├── user.py               # Pydantic schemas for auth
│   │   └── transaction.py        # Pydantic schemas for transactions
│   ├── tasks/
│   │   └── reports.py            # Celery async tasks
│   └── main.py                   # FastAPI app entrypoint
├── migrations/                   # Alembic migrations
├── tests/
│   ├── conftest.py               # Test setup (SQLite, async client)
│   ├── test_auth.py              # Auth endpoint tests
│   └── test_transactions.py      # Transaction endpoint tests
├── docker-compose.yml
├── Dockerfile
├── requirements.txt
└── .env

## Architecture Decisions

- **Async throughout** — FastAPI + asyncpg + SQLAlchemy async for non-blocking I/O
- **Celery + Redis** — heavy operations (report generation) offloaded to background workers
- **Dependency injection** — `get_current_user` reused across all protected endpoints via FastAPI `Depends`
- **TDD** — tests written before implementation; SQLite used in tests for speed and isolation
- **Per-user data isolation** — all queries filtered by `user_id` at the database level