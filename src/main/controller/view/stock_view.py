from typing import Optional
from pydantic import BaseModel, ConfigDict, Field, RootModel


class Stock(BaseModel):
    model_config = ConfigDict(from_attributes=True, str_to_lower=True)

    customer: str
    product_name: Optional[str]
    serial_id: Optional[str]
    color: Optional[str]
    supplier_name: Optional[str]
    with_problems: Optional[bool] = False
    reserved: Optional[bool] = False
    buy_date: Optional[int] = Field(ge=1276704813) # 2010
    buy_price: Optional[float] = Field(ge=0)
    selled: Optional[bool] = False

class Stocks(RootModel):
    root: list[Stock]

    def __iter__(self):
        return iter(self.root)
