from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from src.db.session import get_session

from src.expenses.service import get_expense,create_expense,update_expense,delete_expense,get_expenses
from src.expenses.schema import ExpenseCreate, ExpenseUpdate, ExpenseRead

router = APIRouter(prefix="/expenses", tags=["expenses"])



@router.post("", response_model=ExpenseRead, status_code=status.HTTP_201_CREATED)
async def add_expense(
    expense_data: ExpenseCreate,
    db: AsyncSession = Depends(get_session),
    user_id: int = Depends(get_current_user_id),
):
    return await create_expense(db, expense_data, user_id)


@router.get("", response_model=list[ExpenseRead])
async def list_expenses(
    db: AsyncSession = Depends(get_session),
    user_id: int = Depends(get_current_user_id),
):
    return await get_expenses(db, user_id)


@router.get("/{expense_id}", response_model=ExpenseRead)
async def read_expense(
    expense_id: int,
    db: AsyncSession = Depends(get_session),
    user_id: int = Depends(get_current_user_id),
):
    expense = await get_expense(db, expense_id, user_id)
    if expense is None:
        raise HTTPException(status_code=404, detail="Expense not found")
    return expense


@router.put("/{expense_id}", response_model=ExpenseRead)
async def edit_expense(
    expense_id: int,
    expense_data: ExpenseUpdate,
    db: AsyncSession = Depends(get_session),
    user_id: int = Depends(get_current_user_id),
):
    expense = await get_expense(db, expense_id, user_id)
    if expense is None:
        raise HTTPException(status_code=404, detail="Expense not found")
    return await update_expense(db, expense, expense_data)


@router.delete("/{expense_id}", status_code=status.HTTP_204_NO_CONTENT)
async def remove_expense(
    expense_id: int,
    db: AsyncSession = Depends(get_session),
    user_id: int = Depends(get_current_user_id),
):
    expense = await get_expense(db, expense_id, user_id)
    if expense is None:
        raise HTTPException(status_code=404, detail="Expense not found")
    await delete_expense(db, expense)