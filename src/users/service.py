from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from users.schema import UserCreate, UserLogin
from users.models import User
from users.security import hash_password,verify_password

async def register_user(user_data: UserCreate, session: AsyncSession) -> User:
    stmt = select(User).where(User.email==user_data.email)
    result = await session.execute(stmt) 

    existing_user = result.scalar_one_or_none()
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already exists"
        )
    
    new_user = User(
        username=user_data.username,
        email=user_data.email,
        password=hash_password(user_data.password) 
    ) 
    
    session.add(new_user)
    await session.commit()
    await session.refresh(new_user)

    return new_user


async def login_user(login_data: UserLogin, session: AsyncSession):
    stmt = select(User).where(User.email==login_data.email)
    result = await session.execute(stmt) 
    user = result.scalar_one_or_none()

    if not user:
        raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid credentials"

    )

    if not verify_password(login_data.password, user.password):
        raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid credentials"
    )
    return {
    "message": "Login successful"
}


    



        
    

