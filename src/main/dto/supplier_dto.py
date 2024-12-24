from __future__ import annotations

import secrets

from pydantic import BaseModel, ConfigDict, Field


def random_color_generator():
    color = secrets.randbelow(2**24)
    hex_color = hex(color)
    return "#" + hex_color[2:]


class Supplier(BaseModel):
    model_config = ConfigDict(from_attributes=True, str_strip_whitespace=True, str_to_upper=True, use_enum_values=True)

    id: int | None = None
    name: str = Field(min_length=1)
    color: str | None = random_color_generator()
