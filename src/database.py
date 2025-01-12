from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine
from sqlalchemy.orm import DeclarativeBase

from src.config import settings


engine = create_async_engine(settings.db_url, echo=True) # включение логов бд

async_session_maker = async_sessionmaker(bind=engine, expire_on_commit=False)


class Base(DeclarativeBase):
    pass