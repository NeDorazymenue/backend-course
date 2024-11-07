from pydantic import BaseModel
from typing import Annotated
from fastapi import Query, Depends


class PaginationParams(BaseModel):
    page: Annotated[int | None, Query(1, ge=1)]
    per_page: Annotated[int | None, Query(3, ge=1, lt=30)]


PaginationDep = Annotated[PaginationParams, Depends()]