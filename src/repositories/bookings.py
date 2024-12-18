from src.models.rooms import RoomsOrm
from src.repositories.base import BaseRepository
from src.models.bookings import BookingsOrm
from src.schemas.bookings import Booking, BookingAdd, BookingRequestAdd
from sqlalchemy import select



class BookingsRepository(BaseRepository):
    model = BookingsOrm
    schema = Booking

