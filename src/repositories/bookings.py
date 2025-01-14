from src.repositories.base import BaseRepository
from src.models.bookings import BookingsOrm
from src.repositories.mappers.base import DataMapper
from src.repositories.mappers.mappers import BookingDataMapper



class BookingsRepository(BaseRepository):
    model = BookingsOrm
    mapper: DataMapper = BookingDataMapper

