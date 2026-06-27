# Finance Tracker API

A personal finance REST API built with modern Python backend stack.

## Tech Stack

- **FastAPI** — async REST API framework
- **PostgreSQL** — relational database
- **SQLAlchemy 2.0** — async ORM with Alembic migrations
- **Celery + Redis** — async task queue for report generation
- **Docker Compose** — containerized development environment

## Features

- ✅ Full CRUD for financial transactions (income & expenses)
- ✅ Filter transactions by type and category
- ✅ Real-time balance summary
- ✅ Async monthly report generation via Celery
- ✅ Report status tracking by task ID
- ✅ Auto-generated API docs (Swagger UI)
- ✅ Input validation via Pydantic schemas
- ✅ Database migrations via Alembic

## Getting Started

### Prerequisites
- Docker & Docker Compose

### Run locally

```bash
git clone https://github.com/yourusername/finance-tracker-api.git
cd finance-tracker-api/finance_tracker
docker compose up --build
```

Then open: `http://localhost:8000/docs`

### Run database migrations

```bash
docker compose exec api alembic upgrade head
```

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/transactions/` | Create transaction |
| GET | `/transactions/` | List transactions (with filters) |
| GET | `/transactions/summary` | Income vs expenses balance |
| GET | `/transactions/{id}` | Get single transaction |
| PATCH | `/transactions/{id}` | Update transaction |
| DELETE | `/transactions/{id}` | Delete transaction |
| POST | `/transactions/reports/monthly` | Generate monthly report (async) |
| GET | `/transactions/reports/monthly/{task_id}/status` | Check report status |

## Project Structure

```
finance_tracker/
├── app/
│   ├── api/endpoints/    # Route handlers
│   ├── core/             # Config & settings
│   ├── db/               # Database connection
│   ├── models/           # SQLAlchemy models
│   ├── schemas/          # Pydantic schemas
│   ├── services/         # Business logic
│   └── tasks/            # Celery async tasks
├── migrations/           # Alembic migrations
├── docker-compose.yml
├── Dockerfile
└── requirements.txt
```