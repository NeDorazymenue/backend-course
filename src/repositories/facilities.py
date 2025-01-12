from src.repositories.base import BaseRepository
from src.models.facilities import FacilitiesOrm, RoomsFacilitiesOrm
from src.schemas.facilities import Facility, RoomFacility
from sqlalchemy import select, insert, update, delete



class FacilitiesRepository(BaseRepository):
    model = FacilitiesOrm
    schema = Facility


class RoomsFacilitiesRepository(BaseRepository):
    model = RoomsFacilitiesOrm
    schema = RoomFacility

    async def update_facilities(self, room_id: int, new_facilities: list[int]):
        result = await self.session.execute(
            select(self.model.facility_id).where(self.model.room_id == room_id)
        )
        current_facilities = {row[0] for row in result.fetchall()}  # Текущие facility_id в базе
        new_facilities_set = set(new_facilities)
        to_add = new_facilities_set - current_facilities  # Новые значения, которых нет в базе
        to_delete = current_facilities - new_facilities_set  # Устаревшие значения, которых нет в массиве
        if to_delete:
            await self.session.execute(
                delete(self.model)
                .where(self.model.room_id == room_id)
                .where(self.model.facility_id.in_(to_delete))
            )
        if to_add:
            values_to_add = [{"room_id": room_id, "facility_id": facility_id} for facility_id in to_add]
            await self.session.execute(
                insert(self.model).values(values_to_add)
            )



