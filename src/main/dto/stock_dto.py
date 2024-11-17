from enum import Enum
from typing import Optional
from pydantic import BaseModel, ConfigDict, Field

from src.main.dto.product_dto import Product
from src.main.dto.supplier_dto import Supplier


class StockStates(str, Enum):
    AVAILABLE = "AVAILABLE"
    RESERVED = "RESERVED"
    DEFECTS = "DEFECTS"
    BROKEN = "BROKEN"


class ResponseStock(BaseModel):
    model_config = ConfigDict(from_attributes=True, str_strip_whitespace=True, str_to_upper=True, use_enum_values=True)

    id: Optional[int] = None
    product: Optional[Product] = None
    serial_id: Optional[str] = None
    color: Optional[str] = None
    battery_percent: Optional[int] = None
    state: Optional[StockStates] = StockStates.AVAILABLE
    buy_price: Optional[float] = Field(ge=0, default=None)
    sell_price: Optional[float] = Field(ge=0, default=None)
    supplier: Optional[Supplier] = None
    observations: Optional[str] = None


class UpdateStock(BaseModel):
    model_config = ConfigDict(from_attributes=True, str_strip_whitespace=True, str_to_upper=True, use_enum_values=True)

    id: int
    serial_id: Optional[str] = None
    battery_percent: Optional[int] = None
    sell_price: Optional[float] = Field(ge=0, default=None)
    color: Optional[str] = None
    state: Optional[StockStates] = None
    observations: Optional[str] = None
