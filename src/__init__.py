from fastapi import FastAPI

app = FastAPI(title="Expense Tracker API")

@app.get("/")
async def root():
    return {"message": "Welcome"}
