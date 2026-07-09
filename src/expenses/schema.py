from datetime import datetime
from pydantic import BaseModel

class ExpenseCreate(BaseModel):
    title: str
    amount: float
    category: str | None = None
    description: str | None = None

class ExpenseRead(BaseModel):
    id: int
    title: str
    amount: float
    category: str |  None
    decription: str | None 
    created_at: datetime
    user_id: int

    model_config = {"from_attributes": True}

class ExpenseUpdate(BaseModel):
    title: str | None = None
    amount: float | None = None
    category: str | None = None
    description: str | None = None
    


