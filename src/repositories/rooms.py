from src.repositories.base import BaseRepository
from src.models.rooms import RoomsOrm
from src.schemas.rooms import Rooms
from sqlalchemy import select, func


class RoomsRepository(BaseRepository):
    model = RoomsOrm
    schema = Rooms

    async def get_all_rooms(
            self,
            hotel_id,
            title,
            price,
            quantity,
            limit,
            offset,
    ) -> list[Rooms]:
        query = select(RoomsOrm)
        if hotel_id is not None:
            query = query.filter(RoomsOrm.hotel_id == hotel_id)
        if title is not None:
            query = query.filter(func.lower(RoomsOrm.title).contains(title.strip().lower()))
        if price is not None:
            query = query.filter(RoomsOrm.price == price)
        if quantity is not None:
            query = query.filter(RoomsOrm.quantity == quantity)
        query = (
            query
            .limit(limit)
            .offset(offset)
        )
        result = await self.session.execute(query)
        print(str(query))

        return [Rooms.model_validate(rooms, from_attributes=True) for rooms in result.scalars().all()]

