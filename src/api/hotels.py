from fastapi import Query, APIRouter, Body

from src.api.dependencies import PaginationDep
from src.database import async_session_maker, engine
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
async def add_hotel(hotel_data: Hotel = Body(openapi_examples={
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
async def edit_hotel(hotel_id: int, hotel_data: Hotel):
    async with async_session_maker() as session:
        await HotelsRepository(session).edit(data=hotel_data, id=hotel_id)
        await session.commit()

    return {"status": "OK"}


@router.patch("/{hotel_id}", summary="Частичное обновление данных об отеле")
async def partially_edit_hotel(hotel_id: int, hotel_data: HotelPATCH):
    async with async_session_maker() as session:
        await HotelsRepository(session).edit(data=hotel_data, exclude_unset=True, id=hotel_id)
        await session.commit()
    return {"status": "OK"}


@router.delete("/{hotel_id}", summary="Удаление отеля из базы данных")
async def delete_hotel(hotel_id: int):
    async with async_session_maker() as session:
        await HotelsRepository(session).delete(id=hotel_id)
        await session.commit()
    return {"status": "OK"}

@router.get("/{hotels_id}", summary="Получение отеля по id")
async def  get_one_hotel(hotel_id: int):
    async with async_session_maker() as session:
        hotel = await HotelsRepository(session).get_one_or_none(id=hotel_id)
        return hotel


