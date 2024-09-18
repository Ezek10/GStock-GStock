import time
from sqlalchemy import BigInteger, Column, Integer, String

from src.main.repository.config import Base


class SellerDB(Base):
    __tablename__ = "seller"

    id = Column(Integer, primary_key=True, nullable=False, autoincrement="auto")
    customer = Column(Integer, nullable=False)
    name = Column(String)
    email = Column(String)
    cellphone = Column(String)
    address = Column(String)
    document = Column(String)

    created_at = Column(BigInteger, default=time.time)
    modified_at = Column(BigInteger, onupdate=time.time)

    def __repr__(self):
        return f"SellerDB({self.id})"
