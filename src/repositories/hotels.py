from datetime import date
from typing import Optional

from src.models.rooms import RoomsOrm
from src.repositories.base import BaseRepository
from src.models.hotels import HotelsOrm
from sqlalchemy import select, func

from src.repositories.utils import rooms_ids_for_booking
from src.schemas.hotels import Hotel


class HotelsRepository(BaseRepository):
    model = HotelsOrm
    schema = Hotel

    async def get_all(
            self,
            title,
            location,
            limit,
            offset,
    ) -> list[Hotel]:
        query = select(HotelsOrm)
        if title is not None:
            query = query.filter(func.lower(HotelsOrm.title).contains(title.strip().lower()))
        if location is not None:
            query = query.filter(func.lower(HotelsOrm.location).contains(location.strip().lower()))
        query = (
            query
            .limit(limit)
            .offset(offset)
        )
        result = await self.session.execute(query)

        return [Hotel.model_validate(hotel, from_attributes=True) for hotel in result.scalars().all()]

    async def get_filtered_by_time(
            self,
            date_from: date,
            date_to: date,
            title: Optional[str] = None,
            location: Optional[str] = None,
            limit: Optional[int] = None,
            offset: Optional[int] = None,
    ):
        rooms_ids_to_get = rooms_ids_for_booking(date_from=date_from, date_to=date_to)
        hotels_ids_to_get = (
            select(RoomsOrm.hotel_id)
            .select_from(RoomsOrm)
            .filter(RoomsOrm.id.in_(rooms_ids_to_get))
        )
        if title is not None:
            hotels_ids_to_get = hotels_ids_to_get.filter(
                func.lower(HotelsOrm.title)
                .contains(title.strip().lower())
            )
        if location is not None:
            hotels_ids_to_get = hotels_ids_to_get.filter(
                func.lower(HotelsOrm.location)
                .contains(location.strip().lower())
            )
        hotels_ids_to_get = (
            hotels_ids_to_get
            .limit(limit)
            .offset(offset)
        )
        return await self.get_filtered(HotelsOrm.id.in_(hotels_ids_to_get))




