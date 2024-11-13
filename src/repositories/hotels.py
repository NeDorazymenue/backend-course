from src.repositories.base import BaseRepository
from src.models.hotels import HotelsOrm
from sqlalchemy import select, func

class HotelsRepository(BaseRepository):
    model = HotelsOrm

    async def get_all(
            self,
            title,
            location,
            limit,
            offset,
    ):
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
        return result.scalars().all()




