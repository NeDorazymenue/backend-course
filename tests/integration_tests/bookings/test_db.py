from datetime import date

from src.schemas.bookings import BookingAdd



async def test_booking_crud(db):
    user_id = (await db.users.get_all())[0].id
    room_id = (await db.rooms.get_all())[0].id
    booking_data = BookingAdd(
        user_id=user_id,
        room_id=room_id,
        date_from=date(2025, 8, 8),
        date_to=date(2025, 8, 18),
        price=100,
    )
    booking = await db.bookings.add(booking_data)

    booking_data_in_db = (await db.bookings.get_filtered(id=booking.id))[0]
    assert booking_data_in_db==booking

    booking_data.price = 300
    await db.bookings.edit(data=booking_data, exclude_unset=True, id=booking.id)
    update_booking_data = (await db.bookings.get_filtered(id=booking.id))[0]
    assert update_booking_data.price == booking_data.price

    await db.bookings.delete(id=booking.id)
    deleted_booking = await db.bookings.get_filtered(id=booking.id)
    assert deleted_booking==[]

    await db.commit()