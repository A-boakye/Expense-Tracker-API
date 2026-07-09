from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from src.db.session import get_session
from src.users.schema import UserCreate, UserLogin
from src.users.service import register_user,login_user


auth_router = APIRouter(prefix="/users", tags=["users"])

@auth_router.post("/register")
async def register(
    user: UserCreate,
    session: AsyncSession = Depends(get_session)
):
    return await register_user(user, session)

    
@auth_router.post("/login")
async def login(
    credentials: UserLogin,
    session: AsyncSession = Depends(get_session)
):
    return await login_user(credentials, session)