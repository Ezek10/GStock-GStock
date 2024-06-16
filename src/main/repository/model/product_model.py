import time
from sqlalchemy import BigInteger, Column, Integer, String

from src.main.repository.config import Base


class ProductDB(Base):
    __tablename__ = "product"

    id = Column(Integer, primary_key=True, nullable=False)
    customer = Column(String, nullable=False)
    name = Column(String, nullable=False)
    create_at = Column(BigInteger, default_factory=time.time)
    modified_at = Column(BigInteger, default=time.time, onupdate=time.time)

    def __repr__(self):
        return f"ProductDB({self.id})"
