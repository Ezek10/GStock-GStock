from __future__ import annotations

from enum import Enum
from typing import TYPE_CHECKING

from pydantic import BaseModel, ConfigDict, Field

if TYPE_CHECKING:
    from src.main.dto.product_dto import Product
    from src.main.dto.supplier_dto import Supplier


class StockStates(str, Enum):
    AVAILABLE = "AVAILABLE"
    RESERVED = "RESERVED"
    DEFECTS = "DEFECTS"
    BROKEN = "BROKEN"


class ResponseStock(BaseModel):
    model_config = ConfigDict(from_attributes=True, str_strip_whitespace=True, str_to_upper=True, use_enum_values=True)

    id: int | None = None
    product: Product | None = None
    serial_id: str | None = None
    color: str | None = None
    battery_percent: int | None = None
    state: StockStates | None = StockStates.AVAILABLE
    buy_price: float | None = Field(ge=0, default=None)
    sell_price: float | None = Field(ge=0, default=None)
    supplier: Supplier | None = None
    observations: str | None = None


class UpdateStock(BaseModel):
    model_config = ConfigDict(from_attributes=True, str_strip_whitespace=True, str_to_upper=True, use_enum_values=True)

    id: int
    serial_id: str | None = None
    battery_percent: int | None = None
    sell_price: float | None = Field(ge=0, default=None)
    color: str | None = None
    state: StockStates | None = None
    observations: str | None = None
