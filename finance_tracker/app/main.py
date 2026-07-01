from fastapi import FastAPI
from app.api.endpoints.transactions import router as transactions_router
from app.api.endpoints.auth import router as auth_router

app = FastAPI(
    title="Finance Tracker API",
    description="Personal finance tracker — built with FastAPI, PostgreSQL, Celery & Redis",
    version="1.0.0"
)

app.include_router(auth_router, prefix="/auth", tags=["auth"])
app.include_router(transactions_router, prefix="/transactions", tags=["transactions"])

@app.get("/health")
async def health_check():
    return {"status": "ok"}