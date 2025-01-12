from fastapi import APIRouter

from src.api.dependencies import DBDep
from src.schemas.facilities import FacilityAdd


router = APIRouter(prefix="/facilities", tags=["Удобства"])

@router.get("", summary="Получение всех удобств из базы знаний")
async def get_facilities(db: DBDep):
    return await db.facilities.get_all()


@router.post("", summary="Добавление удобства в базу данных")
async def add_facility(facility_data: FacilityAdd, db: DBDep,):
    facility = await db.facilities.add(facility_data)
    await db.commit()
    return {"status": "OK", "data": facility}