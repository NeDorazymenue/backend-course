from fastapi import APIRouter, Query

from src.api.dependencies import PaginationDep
from src.database import async_session_maker
from src.repositories.rooms import RoomsRepository
from src.schemas.rooms import RoomsAdd, RoomsRequestAdd, Rooms, RoomsPATCH

router = APIRouter(prefix="/hotels", tags=["Номера"])


@router.get("/{hotel_id}/rooms", summary="Получение всех номеров отеля из базы данных")
async def get_rooms(
        pagination: PaginationDep,
        hotel_id: int,
        title: str | None = Query(None,description="Название номера"),
        price : int | None = Query(None, description="Цена"),
        quantity : int | None = Query(None, description="Количество"),
):
    per_page = pagination.per_page or 5
    async with async_session_maker() as session:
        return await RoomsRepository(session).get_all_rooms(
            hotel_id=hotel_id,
            title=title,
            price=price,
            quantity=quantity,
            limit=per_page,
            offset=(pagination.page - 1) * per_page,
        )



@router.post("/{hotel_id}/rooms")
async def add_room(
        room_data: RoomsAdd,
):
    async with async_session_maker() as session:
        room = await RoomsRepository(session).add(room_data)
        await session.commit()
    return {"status": "OK", "data": room}


@router.put("/{hotel_id}/rooms/{room_id}", summary="Полное обновление данных о номере в отеле")
async def edit_room(
        hotel_id: int,
        room_id: int,
        hotel_data: RoomsRequestAdd,
):
    async with async_session_maker() as session:
        await RoomsRepository(session).edit(data=hotel_data, hotel_id=hotel_id, id=room_id)
        await session.commit()

    return {"status": "OK"}


@router.patch("/{hotel_id}/rooms/{room_id}", summary="Частичное обновление данных об номере в отеле")
async def partially_edit_hotel(
        hotel_id: int,
        room_id: int,
        room_data: RoomsPATCH
):
    async with async_session_maker() as session:
        await RoomsRepository(session).edit(data=room_data, exclude_unset=True, hotel_id=hotel_id, id=room_id)
        await session.commit()
    return {"status": "OK"}


@router.delete("/{hotel_id}/rooms/{room_id}", summary="Удаление номера отеля из базы данных")
async def delete_hotel(hotel_id: int, room_id: int):
    async with async_session_maker() as session:
        await RoomsRepository(session).delete(hotel_id=hotel_id, id=room_id)
        await session.commit()
    return {"status": "OK"}
