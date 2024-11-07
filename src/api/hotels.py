from fastapi import Query, APIRouter

from src.api.dependencies import PaginationDep
from src.schemas.hotels import Hotel, HotelPATCH

router = APIRouter(prefix="/hotels", tags=["Отели"])


hotels = [
    {"id": 1, "title": "Sochi", "name": "sochi"},
    {"id": 2, "title": "Дубай", "name": "dubai"},
    {"id": 3, "title": "Мальдивы", "name": "maldivi"},
    {"id": 4, "title": "Геленджик", "name": "gelendzhik"},
    {"id": 5, "title": "Москва", "name": "moscow"},
    {"id": 6, "title": "Казань", "name": "kazan"},
    {"id": 7, "title": "Санкт-Петербург", "name": "spb"},
]

@router.get("", summary="Получение всех отелей из базы данных")
def get_hotels(
        pagination: PaginationDep,
        id: int | None = Query(None, description="Айдишник"),
        title: str | None = Query(None,description="Название отеля"),
        name: str | None = Query(None, description="Типо имя"),
):
    hotels_ = []
    start = (pagination.page - 1) * pagination.per_page
    end = start + pagination.per_page
    for hotel in hotels:
        if id is not None and hotel["id"] != id:
            continue
        if title is not None and hotel["title"] != title:
            continue
        if name is not None and hotel["name"] != name:
            continue
        hotels_.append(hotel)
    return hotels_[start:end]


@router.delete("/{hotel_id}", summary="Удаление отеля из базы данных")
def get_hotels(hotel_id: int):
    global hotels
    hotels = [hotel for hotel in hotels if hotel["id"] != hotel_id]
    return {"status": "OK"}


@router.post("", summary="Добавление отеля в базу данных")
def create_hotel(hotel_data: Hotel):
    global hotels
    hotels.append({
        "id": hotels[-1]["id"] + 1,
        "title": hotel_data.title,
        "name": hotel_data.name,
    })
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