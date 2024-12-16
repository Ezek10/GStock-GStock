from __future__ import annotations

from typing import TYPE_CHECKING

from pydantic import BaseModel, ConfigDict, Field

if TYPE_CHECKING:
    from src.main.dto.supplier_dto import Supplier


class Product(BaseModel):
    model_config = ConfigDict(from_attributes=True, str_strip_whitespace=True, str_to_upper=True, use_enum_values=True)

    id: int | None = None
    name: str = Field(min_length=1)
    list_price: float | None = None


class UpdateProduct(Product):
    name: str | None = None
    id: int


class ResponseStock(BaseModel):
    model_config = ConfigDict(from_attributes=True, str_strip_whitespace=True, str_to_upper=True, use_enum_values=True)

    id: int | None = None
    serial_id: str | None = None
    color: str | None = None
    battery_percent: int | None = None
    state: str
    buy_price: float | None = None
    supplier: Supplier | None = None
    sell_price: float | None = None
    observations: str | None = None
    missing_data: bool = False


class ProductStock(Product):
    stocks: list[ResponseStock] | None = None
    warning_stock: bool | None = None
