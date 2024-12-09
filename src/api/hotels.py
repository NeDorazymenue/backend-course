from fastapi import Query, APIRouter, Body

from src.api.dependencies import PaginationDep, DBDep
from src.schemas.hotels import HotelPatch, HotelAdd

router = APIRouter(prefix="/hotels", tags=["Отели"])


@router.get("", summary="Получение всех отелей из базы данных")
async def get_hotels(
        pagination: PaginationDep,
        db: DBDep,
        title: str | None = Query(None,description="Название отеля"),
        location : str | None = Query(None, description="Адресс")
):
    per_page = pagination.per_page or 5
    return await db.hotels.get_all(
        title=title,
        location=location,
        limit= per_page,
        offset=(pagination.page - 1) * per_page,
    )


@router.get("/{hotel_id}", summary="Получение отеля по id")
async def  get_one_hotel(hotel_id: int, db: DBDep):
    return await db.hotels.get_one_or_none(id=hotel_id)


@router.post("", summary="Добавление отеля в базу данных")
async def add_hotel(
        db: DBDep,
        hotel_data: HotelAdd = Body(openapi_examples={
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
    hotel = await db.hotels.add(hotel_data)
    await db.commit()
    return {"status": "OK", "data": hotel}


@router.put("/{hotel_id}", summary="Полное обновление данных об отеле")
async def edit_hotel(
        hotel_id: int,
        hotel_data: HotelAdd,
        db:DBDep,
):
    await db.hotels.edit(data=hotel_data, id=hotel_id)
    await db.commit()
    return {"status": "OK"}


@router.patch("/{hotel_id}", summary="Частичное обновление данных об отеле")
async def partially_edit_hotel(
        hotel_id: int,
        hotel_data: HotelPatch,
        db: DBDep,
):

    await db.hotels.edit(data=hotel_data, exclude_unset=True, id=hotel_id)
    await db.hotels.commit()
    return {"status": "OK"}


@router.delete("/{hotel_id}", summary="Удаление отеля из базы данных")
async def delete_hotel(hotel_id: int, db: DBDep):
    await db.hotels.delete(id=hotel_id)
    await db.hotels.commit()
    return {"status": "OK"}





