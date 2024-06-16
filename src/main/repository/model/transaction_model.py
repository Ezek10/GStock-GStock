import time
from sqlalchemy import BigInteger, Column, Float, Integer, String

from src.main.repository.config import Base


class TransactionDB(Base):
    __tablename__ = "transaction"

    id = Column(Integer, primary_key=True, nullable=False)
    customer = Column(String, nullable=False)
    client_id = Column(Integer, nullable=False)
    provider_id = Column(Integer, nullable=False)
    total = Column(Float)
    payment_method = Column(String) # hacer enum
    type = Column(String) # hacer enum
    date = Column(BigInteger, default_factory=time.time)

    create_at = Column(BigInteger, default_factory=time.time)
    modified_at = Column(BigInteger, default=time.time, onupdate=time.time)

    def __repr__(self):
        return f"TransactionDB({self.id})"
