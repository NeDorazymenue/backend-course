from fastapi import APIRouter, Body

from src.api.dependencies import DBDep
from src.schemas.facilities import RoomFacilityAdd
from src.schemas.rooms import RoomAdd, RoomRequestAdd, RoomPatch, RoomRequestPatch


router = APIRouter(prefix="/hotels", tags=["Номера"])


@router.get("/{hotel_id}/rooms", summary="Получение всех номеров отеля")
async def get_rooms(hotel_id: int, db:DBDep):
    return await db.rooms.get_filtered(hotel_id=hotel_id)


@router.get("/{hotel_id}/rooms/{room_id}", summary="Получение номера отеля по id")
async def get_room(hotel_id: int, room_id: int, db: DBDep):
    return await db.rooms.get_one_or_none(id=room_id, hotel_id=hotel_id)


@router.post("/{hotel_id}/rooms", summary="Добавление номера отеля")
async def create_room(
        hotel_id: int,
        db:DBDep,
        room_data: RoomRequestAdd = Body(),
):
    _room_data = RoomAdd(hotel_id=hotel_id, **room_data.model_dump())
    room = await db.rooms.add(_room_data)
    rooms_facilities_data = [RoomFacilityAdd(room_id=room.id, facility_id=f_id) for f_id in room_data.facilities_ids]
    await db.rooms_facilities.add_bulk(rooms_facilities_data)
    await db.commit()
    return {"status": "OK", "data": room}


@router.put("/{hotel_id}/rooms/{room_id}", summary="Измение данных о номера")
async def edit_room(hotel_id: int, room_id: int, room_data: RoomRequestAdd, db:DBDep):
    _room_data = RoomAdd(hotel_id=hotel_id, **room_data.model_dump())
    await db.rooms.edit(_room_data, id=room_id)
    new_facilities_data = [f_id for f_id in room_data.facilities_ids]
    await db.rooms_facilities.update_facilities(room_id=room_id, new_facilities=new_facilities_data)
    await db.commit()
    return {"status": "OK"}


@router.patch("/{hotel_id}/rooms/{room_id}", summary="Измение некоторых данных о номера")
async def partially_edit_room(
        hotel_id: int,
        room_id: int,
        room_data: RoomRequestPatch,
        db: DBDep,
):
    _room_data = RoomPatch(hotel_id=hotel_id, **room_data.model_dump(exclude_unset=True))
    await db.rooms.edit(_room_data, exclude_unset=True, id=room_id, hotel_id=hotel_id)
    await db.commit()
    return {"status": "OK"}


@router.delete("/{hotel_id}/rooms/{room_id}", summary="Удаление данных о номере")
async def delete_room(hotel_id: int, room_id: int, db: DBDep):
    await db.rooms.delete(id=room_id, hotel_id=hotel_id)
    await db.commit()
    return {"status": "OK"}
