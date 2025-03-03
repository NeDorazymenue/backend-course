import json

import pytest

from httpx import AsyncClient

from src.config import settings
from src.database import Base, engine_null_pool, async_session_maker_null_pool
from src.main import app
from src.models import *
from src.schemas.hotels import HotelAdd
from src.schemas.rooms import RoomAdd
from src.utils.db_manager import DBManager


@pytest.fixture(scope="session", autouse=True)
def check_test_mode():
    assert settings.MODE == "TEST"


@pytest.fixture(scope="session", autouse=True)
async def setup_database(check_test_mode) -> None:
    async with engine_null_pool.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)


@pytest.fixture(scope="session", autouse=True)
async def add_test_data(setup_database) -> None:
    async with DBManager(session_factory=async_session_maker_null_pool) as db:
        with open("tests/mok_hotels.json", "r", encoding="utf-8") as file:
            hotels_data = json.load(file)
            await db.hotels.add_bulk([HotelAdd(**hotel) for hotel in hotels_data])
        with open("tests/mok_rooms.json", "r", encoding="utf-8") as file:
            rooms_data = json.load(file)
            await db.rooms.add_bulk([RoomAdd(**hotel) for hotel in rooms_data])
        await db.commit()

@pytest.fixture(scope="session", autouse=True)
async def register_user(setup_database):
    async with AsyncClient(app=app, base_url="http://test") as ac:
        responce = await ac.post(
            "/auth/register",
        json={
            "email": "kot@pes.com",
            "password": "1234"
        }
        )