from celery import Celery
from sqlalchemy import create_engine, select, func
from sqlalchemy.orm import Session
import os
from dotenv import load_dotenv

load_dotenv()

celery_app = Celery(
    "finance_tracker",
    broker=os.getenv("REDIS_URL"),
    backend=os.getenv("REDIS_URL")
)

def get_sync_db():
    engine = create_engine(os.getenv("SYNC_DATABASE_URL"))
    with Session(engine) as session:
        yield session

@celery_app.task(name="generate_monthly_report")
def generate_monthly_report(year: int, month: int):
    from app.models.transaction import Transaction, TransactionType

    engine = create_engine(os.getenv("SYNC_DATABASE_URL"))
    with Session(engine) as db:
        income_result = db.execute(
            select(func.sum(Transaction.amount))
            .where(Transaction.type == TransactionType.income)
            .where(func.extract("year", Transaction.created_at) == year)
            .where(func.extract("month", Transaction.created_at) == month)
        ).scalar() or 0

        expense_result = db.execute(
            select(func.sum(Transaction.amount))
            .where(Transaction.type == TransactionType.expense)
            .where(func.extract("year", Transaction.created_at) == year)
            .where(func.extract("month", Transaction.created_at) == month)
        ).scalar() or 0

        categories = db.execute(
            select(Transaction.category, func.sum(Transaction.amount))
            .where(Transaction.type == TransactionType.expense)
            .where(func.extract("year", Transaction.created_at) == year)
            .where(func.extract("month", Transaction.created_at) == month)
            .group_by(Transaction.category)
        ).all()

    return {
        "year": year,
        "month": month,
        "total_income": income_result,
        "total_expenses": expense_result,
        "balance": income_result - expense_result,
        "expenses_by_category": {cat: float(amt) for cat, amt in categories}
    }