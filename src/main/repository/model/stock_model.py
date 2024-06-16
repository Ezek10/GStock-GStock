import time
from sqlalchemy import BigInteger, Boolean, Column, Float, Integer, String

from src.main.repository.config import Base


class StockDB(Base):
    __tablename__ = "stock"

    id = Column(Integer, primary_key=True, nullable=False)
    customer = Column(String, nullable=False)
    product_id = Column(Integer, nullable=False)
    supplier_id = Column(Integer, nullable=False)
    serial_id = Column(String)
    color = Column(String)
    with_problems = Column(Boolean, default=False)
    reserved = Column(Boolean, default=False)
    selled = Column(Boolean, default=False)
    buy_date = Column(BigInteger) #epoch
    buy_price = Column(Float)

    create_at = Column(BigInteger, default_factory=time.time)
    modified_at = Column(BigInteger, default=time.time, onupdate=time.time)

    def __repr__(self):
        return f"StockDB({self.id})"
