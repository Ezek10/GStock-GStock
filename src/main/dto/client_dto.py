from __future__ import annotations

from pydantic import BaseModel, ConfigDict, Field


class Client(BaseModel):
    model_config = ConfigDict(from_attributes=True, str_strip_whitespace=True, str_to_upper=True, use_enum_values=True)

    id: int | None = None
    name: str = Field(min_length=1)
    email: str | None = None
    cellphone: str | None = None
    address: str | None = None
    document: str | None = None
