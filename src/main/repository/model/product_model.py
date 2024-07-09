import time
from sqlalchemy import BigInteger, Column, Float, Integer, String
from sqlalchemy.orm import Mapped, relationship
from src.main.repository.config import Base


class ProductDB(Base):
    __tablename__ = "product"

    id = Column(Integer, primary_key=True, nullable=False, autoincrement="auto")
    customer = Column(String, nullable=False)
    name = Column(String, nullable=False)
    list_price = Column(Float)
    created_at = Column(BigInteger, default=time.time)
    modified_at = Column(BigInteger, default=time.time, onupdate=time.time)

    stocks: Mapped[list["StockDB"]] = relationship(back_populates="product", lazy='selectin', single_parent=True)

    def __repr__(self):
        return f"ProductDB({self.id})"
