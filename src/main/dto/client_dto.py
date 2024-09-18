from typing import Optional
from pydantic import BaseModel, ConfigDict, Field


class Client(BaseModel):
    model_config = ConfigDict(from_attributes=True, str_strip_whitespace=True, str_to_upper=True, use_enum_values=True)
    
    id: Optional[int] = None
    name: str = Field(min_length=1)
    email: Optional[str] = None
    cellphone: Optional[int] = None
    address: Optional[str] = None
    document: Optional[str] = None
