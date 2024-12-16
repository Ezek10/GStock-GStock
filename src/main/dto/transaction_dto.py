from __future__ import annotations

from datetime import datetime
from enum import Enum
from typing import TYPE_CHECKING, Literal

from pydantic import BaseModel, ConfigDict, Field, field_validator

from src.main.dto.stock_dto import ResponseStock, StockStates

if TYPE_CHECKING:
    from src.main.dto.client_dto import Client
    from src.main.dto.seller_dto import Seller
    from src.main.dto.supplier_dto import Supplier


class TransactionTypes(str, Enum):
    BUY = "BUY"
    SELL = "SELL"


class PaymentMethods(str, Enum):
    CASH = "CASH"
    DEBIT = "DEBIT"
    CREDIT = "CREDIT"
    CRYPTO = "CRYPTO"
    TRANSFER = "TRANSFER"


class ContactVias(str, Enum):
    REFERED = "REFERED"
    INSTAGRAM = "INSTAGRAM"
    FACEBOOK = "FACEBOOK"
    TIKTOK = "TIKTOK"
    RECURRENT = "RECURRENT"
    OTHER = "OTHER"


class BuyProducts(BaseModel):
    model_config = ConfigDict(from_attributes=True, str_strip_whitespace=True, str_to_upper=True, use_enum_values=True)
    product_name: str
    serial_id: str | None = None
    color: str | None = None
    battery_percent: int | None = None
    state: StockStates | None = StockStates.AVAILABLE
    buy_price: float = Field(gt=0)
    sell_price: float | None = Field(gt=0, default=None)
    observations: str | None = None


class BuyTransaction(BaseModel):
    model_config = ConfigDict(from_attributes=True, str_strip_whitespace=True, str_to_upper=True, use_enum_values=True)
    products: list[BuyProducts] = Field(min_length=1)
    partial_payment: int | None = Field(ge=0)
    type: Literal[TransactionTypes.BUY] = TransactionTypes.BUY
    date: datetime
    payment_method: PaymentMethods | None = None
    supplier: Supplier

    @field_validator("date", mode="after")
    def timestamp_to_int(self, v: datetime):
        return int(v.timestamp()) if isinstance(v, datetime) else v


class SellProduct(BaseModel):
    id: int
    sell_price: float = Field(gt=0)


class SellTransaction(BaseModel):
    model_config = ConfigDict(from_attributes=True, str_strip_whitespace=True, str_to_upper=True, use_enum_values=True)
    products: list[SellProduct] = Field(min_length=1)
    type: Literal[TransactionTypes.SELL] = TransactionTypes.SELL
    partial_payment: int | None = Field(ge=0)
    seller: Seller
    client: Client
    payment_method: PaymentMethods | None = None
    date: datetime
    contact_via: ContactVias | None = ContactVias.OTHER
    has_swap: bool | None = False
    swap_products: list[BuyProducts] | None = None

    @field_validator("date", mode="after")
    def timestamp_to_int(self, v: datetime):
        return int(v.timestamp()) if isinstance(v, datetime) else v


class UpdateBuyTransaction(BuyTransaction):
    id: int


class UpdateSellTransaction(SellTransaction):
    id: int


class ResponseTransaction(BaseModel):
    model_config = ConfigDict(from_attributes=True, str_strip_whitespace=True, str_to_upper=True, use_enum_values=True)

    id: int
    type: TransactionTypes
    total: float
    name: str
    payment_method: PaymentMethods | None = None
    partial_payment: float | None = None
    date: datetime
    contact_via: ContactVias | None = None
    products: list[ResponseStock]
    swap_products: list[ResponseStock] | None = None
    seller: Seller | None
    client: Client | None
    supplier: Supplier | None


class FilterSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True, str_strip_whitespace=True, str_to_upper=True, use_enum_values=True)

    page: int | None = Field(default=1, gt=0)
    filter_by_buy_type: bool | None = False
    filter_by_sell_type: bool | None = False
    filter_by_product: int | None = None
    filter_by_specific_date: int | None = Field(default=None, gt=0, lt=1000000000000000000)
    filter_by_start_date: int | None = Field(default=None, gt=0, lt=1000000000000000000)
    filter_by_end_date: int | None = Field(default=None, gt=0, lt=1000000000000000000)
    filter_by_supplier: int | None = None
    filter_by_client: int | None = None
    filter_by_seller: int | None = None
    filter_by_partial_payment: bool | None = False


class Cards(BaseModel):
    model_config = ConfigDict(from_attributes=True, str_strip_whitespace=True, str_to_upper=True, use_enum_values=True)

    channels: dict[ContactVias, float]
    product_bought: float
    product_sold: float
    earns: int
    sellers: dict[str, int]
