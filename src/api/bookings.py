from fastapi import APIRouter


from src.api.dependencies import DBDep, UserIdDep
from src.schemas.bookings import BookingRequestAdd

router = APIRouter(prefix="/bookings", tags=["Бронирования"])

@router.get("", summary="Получение всех бронирований из базы данных")
async def get_bookings(
        db: DBDep,
        user_id: UserIdDep,
):
    return await db.bookings.get_filtered(user_id=user_id)


@router.post("", summary="Добавление бронирования в базу данных")
async def create_booking(
        db: DBDep,
        user_id: UserIdDep,
        booking_data: BookingRequestAdd,
):
    new_booking = await db.bookings.add_booking(booking_data, user_id)
    await db.commit()
    return {"status": "OK", "data": new_booking}