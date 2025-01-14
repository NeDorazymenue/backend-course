from src.repositories.base import BaseRepository
from src.models.facilities import FacilitiesOrm, RoomsFacilitiesOrm
from src.repositories.mappers.base import DataMapper
from src.repositories.mappers.mappers import FacilityDataMapper
from src.schemas.facilities import Facility, RoomFacility
from sqlalchemy import select, insert, delete



class FacilitiesRepository(BaseRepository):
    model = FacilitiesOrm
    mapper: DataMapper = FacilityDataMapper


class RoomsFacilitiesRepository(BaseRepository):
    model = RoomsFacilitiesOrm
    schema = RoomFacility

    async def update_facilities(self, room_id: int, facilities_ids: list[int]):
        get_current_facilities_ids_query = (
            select(self.model.facility_id)
            .filter_by(room_id=room_id)
        )
        result = await self.session.execute(get_current_facilities_ids_query)
        current_facilities = set(result.scalars().all())
        new_facilities_set = set(facilities_ids)
        ids_to_insert = new_facilities_set - current_facilities
        ids_to_delete = current_facilities - new_facilities_set
        if ids_to_delete:
            delete_m2m_facilities_stmt = (
                delete(self.model)
                .filter(
                    self.model.room_id == room_id,
                    self.model.facility_id.in_(ids_to_delete)
                )
            )
            await self.session.execute(delete_m2m_facilities_stmt)
        if ids_to_insert:
            insert_m2m_facilities_stmt = (
                insert(self.model)
                .values(
                    [{"room_id": room_id, "facility_id": f_id} for f_id in ids_to_insert]
                )
            )
            await self.session.execute(insert_m2m_facilities_stmt)



