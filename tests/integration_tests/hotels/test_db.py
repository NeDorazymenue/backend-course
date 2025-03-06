from src.schemas.hotels import HotelAdd


async def test_add_booking(db):
    hotel_data = HotelAdd(title="Hotel 5 stars", location="Анапа")
    new_hotel_data = await db.hotels.add(hotel_data)
    await db.commit()
