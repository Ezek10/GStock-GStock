from enum import Enum
from typing import Literal, Optional
from pydantic import BaseModel, ConfigDict, Field, field_validator
from datetime import datetime

from src.main.dto.client_dto import Client
from src.main.dto.seller_dto import Seller
from src.main.dto.stock_dto import ResponseStock, StockStates
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
    serial_id: Optional[str] = None
    color: Optional[str] = None
    battery_percent: Optional[int] = None
    state: Optional[StockStates] = StockStates.AVAILABLE
    buy_price: Optional[float] = Field(ge=0, default=None)
    observations: Optional[str] = None


class BuyTransaction(BaseModel):
    model_config = ConfigDict(from_attributes=True, str_strip_whitespace=True, str_to_upper=True, use_enum_values=True)
    products: list[BuyProducts]
    type: Literal[TransactionTypes.BUY] = TransactionTypes.BUY
    date: datetime
    payment_method: Optional[PaymentMethods] = None
    supplier: Supplier

    @field_validator("date", mode="after")
    def timestamp_to_int(cls, v: datetime):
        return int(v.timestamp()) if isinstance(v, datetime) else v


class SellProduct(BaseModel):
    id: int
    sell_price: float


class SellTransaction(BaseModel):
    model_config = ConfigDict(from_attributes=True, str_strip_whitespace=True, str_to_upper=True, use_enum_values=True)
    products: list[SellProduct]
    type: Literal[TransactionTypes.SELL] = TransactionTypes.SELL
    seller: Seller
    client: Client
    payment_method: Optional[PaymentMethods] = None
    date: datetime
    contact_via: Optional[ContactVias] = ContactVias.OTHER
    has_swap: Optional[bool] = False
    swap_products: Optional[list[BuyProducts]] = None

    @field_validator("date", mode="after")
    def timestamp_to_int(cls, v: datetime):
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
    payment_method: Optional[PaymentMethods] = None
    date: datetime
    contact_via: Optional[ContactVias] = None
    products: list[ResponseStock]
    swap_products: Optional[list[ResponseStock]] = None
    seller: Optional[Seller]
    client: Optional[Client]
    supplier: Optional[Supplier]


class FilterSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True, str_strip_whitespace=True, str_to_upper=True, use_enum_values=True)

    page: Optional[int] = Field(default=1, gt=0)
    filter_by_buy_type: Optional[bool] = False
    filter_by_sell_type: Optional[bool] = False
    filter_by_product: Optional[int] = None
    filter_by_specific_date: Optional[int] = Field(default=None, gt=0, lt=1000000000000000000)
    filter_by_start_date: Optional[int] = Field(default=None, gt=0, lt=1000000000000000000)
    filter_by_end_date: Optional[int] = Field(default=None, gt=0, lt=1000000000000000000)
    filter_by_supplier: Optional[int] = None
    filter_by_client: Optional[int] = None
    filter_by_seller: Optional[int] = None


class Cards(BaseModel):
    model_config = ConfigDict(from_attributes=True, str_strip_whitespace=True, str_to_upper=True, use_enum_values=True)

    channels: dict[ContactVias, float]
    product_bought: float
    product_sold: float
    earns: int
    sellers: dict[str, int]
