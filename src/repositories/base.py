from fastapi import HTTPException
from sqlalchemy import select, insert, update, delete
from pydantic import BaseModel


class BaseRepository:
    model = None
    schema: BaseModel = None

    def __init__(self, session):
        self.session = session

    async def check_unique_object(self, **filter_by):
        count_query = (select(self.model).filter_by(**filter_by))
        result = await self.session.execute(count_query)
        rows = result.scalars().all()
        flag = True
        if len(rows) == 0:
            flag = False
            raise HTTPException(status_code=404, detail="объект не найден")
        if len(rows) > 1:
            flag = False
            raise HTTPException(status_code=422, detail="объектов больше одного")
        return flag

    async def get_all(self, *args, **kwargs):
        query = select(self.model)
        result = await self.session.execute(query)
        return [self.schema.model_validate(model, from_attributes=True) for model in result.scalars().all()]


    async def get_one_or_none(self, **filter_by):
        query = select(self.model).filter_by(**filter_by)
        result = await self.session.execute(query)
        model = result.scalars().one_or_none()
        if model is None:
             return None
        return self.schema.model_validate(model, from_attributes=True)



    async def add(self, data: BaseModel):
        add_data_stmt = insert(self.model).values(**data.model_dump()).returning(self.model)
        result = await self.session.execute(add_data_stmt)
        model = result.scalars().one()
        return self.schema.model_validate(model, from_attributes=True)

    async def edit(self, data: BaseModel, exclude_unset: bool = False, **filter_by):
        if await self.check_unique_object(**filter_by):
            update_stmt = (
                update(self.model)
                .filter_by(**filter_by)
                .values(**data.model_dump(exclude_unset=exclude_unset))
                           )
            await self.session.execute(update_stmt)

    async def delete(self, **filter_by):
        if await self.check_unique_object(**filter_by):
            delete_stmt = delete(self.model).filter_by(**filter_by)
            await self.session.execute(delete_stmt)




