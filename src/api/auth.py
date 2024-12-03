from fastapi import APIRouter, Body, HTTPException

from src.database import async_session_maker
from src.repositories.users import UsersRepository

from src.schemas.users import UsersRequestAdd, UserAdd
from passlib.context import CryptContext


router = APIRouter(prefix="/auth", tags=["Авторизация и аутентификация"])

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


@router.post("/register", summary="Регистрация")
async def register_user(data: UsersRequestAdd = Body(openapi_examples={
    "1": {
        "summary": "Пользователь 1",
        "value": {
            "email" : "user1@user.ru",
            "password" : "usEr_1"
        }
    },
    "2": {
        "summary": "Пользователь 2",
        "value": {
            "email" : "user2@user.com",
            "password" : "useR_2"
        }
    }
})):
    hashed_password = pwd_context.hash(data.password)
    new_user_data = UserAdd(email=data.email, hashed_password=hashed_password)
    async with async_session_maker() as session:
        existing_user = await UsersRepository(session).get_one_or_none(email=new_user_data.email)
        if existing_user:
            raise HTTPException(status_code=400, detail="User with this email already exists.")
        await UsersRepository(session).add(new_user_data)
        await session.commit()
    return {"status": "OK"}