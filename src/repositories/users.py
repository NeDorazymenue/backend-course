from src.repositories.base import BaseRepository
from src.models.users import UsersOrm

from src.schemas.hotels import Hotel


class UsersRepository(BaseRepository):
    model = UsersOrm
    schema = Hotel