from pydantic import BaseModel, Field

class RoomsRequestAdd(BaseModel):
    title: str
    description: str | None = Field(None)
    price: int
    quantity: int


class RoomsAdd(RoomsRequestAdd):
    hotel_id: int


class Rooms(RoomsAdd):
    id: int


class RoomsPATCH(BaseModel):
    title: str | None = Field(None)
    description: str | None = Field(None)
    price: int | None = Field(None)
    quantity: int | None = Field(None)
