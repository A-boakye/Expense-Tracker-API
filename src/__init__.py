from contextlib import asynccontextmanager
from fastapi import FastAPI
from .db.session import create_db 
from src.users.models import User 
from src.expenses.models import Expense


@asynccontextmanager
async def lifespan(app: FastAPI):
    print("Starting application...")
    await create_db()
    yield
    print("Stopping application...")




app = FastAPI(title="Expense Tracker API",lifespan=lifespan)

@app.get("/")
async def root():
    return {"message": "Welcome"}


