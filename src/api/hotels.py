from fastapi import Query, APIRouter, Body

from sqlalchemy import insert, select, func

from src.api.dependencies import PaginationDep
from src.database import async_session_maker, engine
from src.models.hotels import HotelsOrm
from src.repositories.hotels import HotelsRepository
from src.schemas.hotels import Hotel, HotelPATCH

router = APIRouter(prefix="/hotels", tags=["Отели"])


@router.get("", summary="Получение всех отелей из базы данных")
async def get_hotels(
        pagination: PaginationDep,
        title: str | None = Query(None,description="Название отеля"),
        location : str | None = Query(None, description="Адресс")
):
    per_page = pagination.per_page or 5
    async with async_session_maker() as session:
        return await HotelsRepository(session).get_all(
            title=title,
            location=location,
            limit= per_page,
            offset=(pagination.page - 1) * per_page,
        )


@router.post("", summary="Добавление отеля в базу данных")
async def create_hotel(hotel_data: Hotel = Body(openapi_examples={
    "1" : {
        "summary": "Сочи",
        "value" : {
            "title" : "Отель 5 звезд у моря",
            "location" : "Сочи и адресс",
        }
    },
    "2" : {
        "summary": "Дубай",
        "value" : {
            "title" : "Отель 6 звезд",
            "location" : "Дубай и адресс",
        }
    },
})
):
    async with async_session_maker() as session:
        hotel = await HotelsRepository(session).add(hotel_data)
        await session.commit()
    return {"status": "OK", "data": hotel}


@router.put("/{hotel_id}", summary="Полное обновление данных об отеле")
async def put_hotel(hotel_id: int, hotel_data: Hotel):
    async with async_session_maker() as session:
        await HotelsRepository(session).edit(data=hotel_data, id=hotel_id)
        await session.commit()

    return {"status": "OK"}


@router.patch("/{hotel_id}", summary="Частичное обновление данных об отеле")
def patch_hotel(hotel_id: int, hotel_data: HotelPATCH):
    global hotels
    for hotel in hotels:
        if hotel["id"] == hotel_id:
            if hotel_data.title is not None:
                hotel["title"] = hotel_data.title
            if hotel_data.name is not None:
                hotel["name"] = hotel_data.name
    return {"status": "OK"}


@router.delete("/{hotel_id}", summary="Удаление отеля из базы данных")
async def get_hotels(hotel_id: int):
    async with async_session_maker() as session:
        await HotelsRepository(session).delete(id=hotel_id)
        await session.commit()
    return {"status": "OK"}
