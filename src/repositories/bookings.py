from src.models.rooms import RoomsOrm
from src.repositories.base import BaseRepository
from src.models.bookings import BookingsOrm
from src.schemas.bookings import Booking, BookingAdd, BookingRequestAdd
from sqlalchemy import select



class BookingsRepository(BaseRepository):
    model = BookingsOrm
    schema = Booking

    async def add_booking(self, booking_data: BookingRequestAdd, user_id: int) -> BookingsOrm:
        result = await self.session.execute(select(RoomsOrm.price).filter(RoomsOrm.id == booking_data.room_id))
        room_price = result.scalars().one_or_none()
        new_booking = BookingsOrm(
            user_id=user_id,
            room_id=booking_data.room_id,
            date_from=booking_data.date_from,
            date_to=booking_data.date_to,
            price=room_price
        )
        new_booking.price = new_booking.total_cost
        self.session.add(new_booking)
        return new_booking

