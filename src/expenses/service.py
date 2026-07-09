from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from src.expenses.models import Expense
from src.expenses.schema import ExpenseCreate, ExpenseUpdate


async def create_expense(db: AsyncSession, expense_data: ExpenseCreate, user_id: int) -> Expense:
    expense = Expense(**expense_data.model_dump(), user_id=user_id)
    db.add(expense)
    await db.commit()
    await db.refresh(expense)
    return expense


async def get_expenses(db: AsyncSession, user_id: int) -> list[Expense]:
    stmt = select(Expense).where(Expense.user_id == user_id)
    result = await db.execute(stmt)
    return list(result.scalars().all())


async def get_expense(db: AsyncSession, expense_id: int, user_id: int) -> Expense | None:
    stmt = select(Expense).where(
        Expense.id == expense_id,
        Expense.user_id == user_id,
    )
    result = await db.execute(stmt)
    return result.scalars().first()


async def update_expense(db: AsyncSession, expense: Expense, expense_data: ExpenseUpdate) -> Expense:
    updates = expense_data.model_dump(exclude_unset=True)
    for key, value in updates.items():
        setattr(expense, key, value)
    await db.commit()
    await db.refresh(expense)
    return expense


async def delete_expense(db: AsyncSession, expense: Expense) -> None:
    await db.delete(expense)
    await db.commit()