from fastapi import Query, Body, APIRouter


router = APIRouter(prefix="/hotels", tags=["Отели"])


hotels = [
    {"id": 1, "title": "Сочи", "name": "sochi"},
    {"id": 2,"title": "Дубай", "name": "dubai"},
]

@router.get("", summary="Получение всех отелей из базы данных")
def get_hotels(
        id: int | None = Query(None, description="Айдишник"),
        title: str | None = Query(None,description="Название отеля"),
):
    hotels_ = []
    for hotel in hotels:
        if id and hotel["id"] != id:
            continue
        if title and hotel["title"] != title:
            continue
        hotels_.append(hotel)
    return hotels_


@router.delete("/{hotel_id}", summary="Удаление отеля из базы данных")
def get_hotels(hotel_id: int):
    global hotels
    hotels = [hotel for hotel in hotels if hotel["id"] != hotel_id]
    return {"status": "OK"}


@router.post("", summary="Добавление отеля в базу данных")
def create_hotel(
        title: str=Body(embed=True),
):
    global hotels
    hotels.append({
        "id": hotels[-1]["id"] + 1,
        "title": title
    })
    return {"status": "OK"}


@router.put("/{hotel_id}", summary="Полное обновление данных об отеле")
def put_hotel(
        hotel_id: int,
        title: str = Body(),
        name: str = Body(),
):
    global hotels
    for hotel in hotels:
        if hotel["id"] == hotel_id:
            hotel["title"] = title
            hotel["name"] = name
    return {"status": "OK"}


@router.patch("/{hotel_id}", summary="Частичное обновление данных об отеле")
def patch_hotel(
        hotel_id: int,
        title: str | None= Body(default=None),
        name: str | None= Body(default=None),
):
    global hotels
    for hotel in hotels:
        if hotel["id"] == hotel_id:
            if title is not None:
                hotel["title"] = title
            if name is not None:
                hotel["name"] = name
    return {"status": "OK"}