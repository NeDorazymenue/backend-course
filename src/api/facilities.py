from fastapi import Query, APIRouter, Body

from src.api.dependencies import DBDep
from src.schemas.facilities import FacilitiesAdd, Facilities


router = APIRouter(prefix="/facilities", tags=["Удобства"])

@router.get("", summary="Получение всех удобств из базы знаний")
async def get_facilities(db: DBDep):
    return await db.facilities.get_all()


@router.post("", summary="Добавление удобства в базу данных")
async def add_facility(data: FacilitiesAdd, db: DBDep,):
    facility = await db.facilities.add(data)
    await db.commit()
    return {"status": "OK", "data": facility}