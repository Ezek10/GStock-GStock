from __future__ import annotations

from typing import Generic, TypeVar

from pydantic import BaseModel

T = TypeVar("T")
Y = TypeVar("Y")


class ResponseSchema(BaseModel, Generic[T]):
    """basic response for any request"""

    detail: str
    result: T | None = None


class PageResponse(BaseModel, Generic[Y]):
    """The response for a pagination query."""

    page_number: int
    page_size: int
    total_pages: int
    total_record: int
    content: list[Y]

    def __eq__(self, value: object) -> bool:
        if type(value) is not PageResponse:
            raise TypeError()
        return self.model_dump() == value.model_dump()
