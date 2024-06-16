import time
from sqlalchemy import BigInteger, Column, Float, Integer, String

from src.main.repository.config import Base


class TransactionProductDB(Base):
    __tablename__ = "transaction_product"

    id = Column(Integer, primary_key=True, nullable=False)
    transaction_id = Column(Integer, nullable=False)
    stock_id = Column(Integer, nullable=False)
    price = Column(Float)

    create_at = Column(BigInteger, default_factory=time.time)
    modified_at = Column(BigInteger, default=time.time, onupdate=time.time)

    def __repr__(self):
        return f"TransactionProductDB({self.id})"
