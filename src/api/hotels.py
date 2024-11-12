from fastapi import Query, APIRouter, Body

from sqlalchemy import insert, select, func

from src.api.dependencies import PaginationDep
from src.database import async_session_maker, engine
from src.models.hotels import HotelsOrm
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
        query = select(HotelsOrm)
        if title is not None:
            # query = query.filter_by(title=title)
            query = query.filter(func.lower(HotelsOrm.title).contains(title.strip().lower()))
        if location is not None:
            # query = query.filter_by(location=location)
            query = query.filter(func.lower(HotelsOrm.location).contains(location.strip().lower()))
        query = (
            query
            .limit(per_page)
            .offset((pagination.page - 1) * per_page)
        )
        result = await session.execute(query)
        hotels = result.scalars().all()

        return hotels


@router.delete("/{hotel_id}", summary="Удаление отеля из базы данных")
def get_hotels(hotel_id: int):
    global hotels
    hotels = [hotel for hotel in hotels if hotel["id"] != hotel_id]
    return {"status": "OK"}


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
        add_hotel_stmt = insert(HotelsOrm).values(**hotel_data.model_dump())
        print(add_hotel_stmt.compile(engine, compile_kwargs={"literal_binds": True}))
        await session.execute(add_hotel_stmt)
        await session.commit()
    return {"status": "OK"}


@router.put("/{hotel_id}", summary="Полное обновление данных об отеле")
def put_hotel(hotel_id: int, hotel_data: Hotel):
    global hotels
    for hotel in hotels:
        if hotel["id"] == hotel_id:
            hotel["title"] = hotel_data.title
            hotel["name"] = hotel_data.name
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