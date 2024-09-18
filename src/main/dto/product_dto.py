from typing import Optional
from pydantic import BaseModel, ConfigDict, Field

from src.main.dto.supplier_dto import Supplier


class Product(BaseModel):
    model_config = ConfigDict(from_attributes=True, str_strip_whitespace=True, str_to_upper=True, use_enum_values=True)
    
    id: Optional[int] = None
    name: str = Field(min_length=1)
    list_price: Optional[float] = None


class UpdateProduct(Product):
    name: Optional[str] = None
    id: int


class ResponseStock(BaseModel):
    model_config = ConfigDict(from_attributes=True, str_strip_whitespace=True, str_to_upper=True, use_enum_values=True)

    id: Optional[int] = None
    serial_id: Optional[str] = None
    color: Optional[str] = None
    battery_percent: Optional[int] = None
    state: str
    buy_price: Optional[float] = None
    supplier: Optional[Supplier] = None
    observations: Optional[str] = None
    missing_data: bool = False


class ProductStock(Product):
    stocks: Optional[list[ResponseStock]] = None
    warning_stock: Optional[bool] = None
