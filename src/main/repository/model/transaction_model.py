import time
from typing import TYPE_CHECKING

from sqlalchemy import BigInteger, Boolean, Column, Float, ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, relationship

from src.main.repository.config import Base

if TYPE_CHECKING:
    from src.main.repository.model.client_model import ClientDB
    from src.main.repository.model.seller_model import SellerDB
    from src.main.repository.model.stock_model import StockDB
    from src.main.repository.model.supplier_model import SupplierDB


class TransactionDB(Base):
    __tablename__ = "transaction"

    id = Column(Integer, primary_key=True, nullable=False, autoincrement="auto")
    customer = Column(Integer, nullable=False)
    client_id = Column(Integer, ForeignKey("client.id"))
    seller_id = Column(Integer, ForeignKey("seller.id"))
    supplier_id = Column(Integer, ForeignKey("supplier.id"))
    payment_method = Column(String)
    partial_payment = Column(Float)
    contact_via = Column(String)
    type = Column(String, nullable=False)
    date = Column(BigInteger, nullable=False)
    has_swap = Column(Boolean)

    supplier: Mapped["SupplierDB"] = relationship(backref="transactions", lazy="selectin", single_parent=True)
    client: Mapped["ClientDB"] = relationship(backref="transactions", lazy="selectin", single_parent=True)
    seller: Mapped["SellerDB"] = relationship(backref="transactions", lazy="selectin", single_parent=True)
    buy_stocks: Mapped[list["StockDB"]] = relationship(
        back_populates="buy_transaction", lazy="selectin", foreign_keys="StockDB.buy_transaction_id"
    )
    sell_stocks: Mapped[list["StockDB"]] = relationship(
        back_populates="sell_transaction", lazy="selectin", foreign_keys="StockDB.sell_transaction_id"
    )

    created_at = Column(BigInteger, default=time.time)
    modified_at = Column(BigInteger, default=time.time, onupdate=time.time)

    def __repr__(self) -> str:
        return f"TransactionDB({self.id})"
