from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from .models import Expense
from .schema import ExpenseCreate, ExpenseUpdate

USER_ID = 1


async def create_expense(
    db: AsyncSession,
    expense_data: ExpenseCreate,
):
    expense = Expense(
        title=expense_data.title,
        amount=expense_data.amount,
        category=expense_data.category,
        description=expense_data.description,
        date=expense_data.date,
        user_id=USER_ID,
    )

    db.add(expense)
    await db.commit()
    await db.refresh(expense)

    return expense


async def get_expenses(db: AsyncSession):
    stmt = select(Expense).where(
        Expense.user_id == USER_ID
    )

    result = await db.execute(stmt)

    return result.scalars().all()


async def get_expense(
    db: AsyncSession,
    expense_id: int,
):
    stmt = select(Expense).where(
        Expense.id == expense_id,
        Expense.user_id == USER_ID,
    )

    result = await db.execute(stmt)

    return result.scalar_one_or_none()


async def update_expense(
    db: AsyncSession,
    expense: Expense,
    expense_data: ExpenseUpdate,
):
    expense.title = expense_data.title
    expense.amount = expense_data.amount
    expense.category = expense_data.category
    expense.description = expense_data.description
    expense.date = expense_data.date

    await db.commit()
    await db.refresh(expense)

    return expense


async def delete_expense(
    db: AsyncSession,
    expense: Expense,
):
    await db.delete(expense)
    await db.commit()