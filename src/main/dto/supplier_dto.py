from typing import Optional
from pydantic import BaseModel, ConfigDict


def random_color_generator():
    return "#B4321"

class Supplier(BaseModel):
    model_config = ConfigDict(from_attributes=True, str_strip_whitespace=True, str_to_upper=True, use_enum_values=True)

    id: Optional[int] = None
    name: str
    color: Optional[str] = random_color_generator()
