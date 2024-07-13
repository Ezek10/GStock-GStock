import time
from sqlalchemy import BigInteger, Column, Float, ForeignKey, Integer, String
from sqlalchemy.orm import relationship, Mapped

from src.main.repository.config import Base


class StockDB(Base):
    __tablename__ = "stock"

    id = Column(Integer, primary_key=True, nullable=False, autoincrement="auto")
    customer = Column(String, nullable=False)
    product_id = Column(Integer, ForeignKey("product.id"), nullable=False)
    buy_transaction_id = Column(Integer, ForeignKey("transaction.id"), nullable=False)
    sell_transaction_id = Column(Integer, ForeignKey("transaction.id"))
    serial_id = Column(String)
    battery_percent = Column(Integer, default=100)
    color = Column(String)
    state = Column(String, nullable=False)
    buy_price = Column(Float, nullable=False)
    sell_price = Column(Float)
    observations = Column(String)

    product: Mapped["ProductDB"] = relationship(back_populates="stocks", lazy='selectin', single_parent=True)
    buy_transaction: Mapped["TransactionDB"] = relationship(back_populates="buy_stocks", lazy='selectin', foreign_keys=buy_transaction_id)
    sell_transaction: Mapped["TransactionDB"] = relationship(back_populates="sell_stocks", lazy='selectin', foreign_keys=sell_transaction_id)
    supplier: Mapped["SupplierDB"] = relationship(secondary="transaction", primaryjoin="stock.c.buy_transaction_id==transaction.c.id", secondaryjoin="transaction.c.supplier_id==supplier.c.id", backref="stocks", lazy='selectin', viewonly=True)

    created_at = Column(BigInteger, default=time.time)
    modified_at = Column(BigInteger, default=time.time, onupdate=time.time)

    def __repr__(self):
        return f"StockDB({self.id})"
