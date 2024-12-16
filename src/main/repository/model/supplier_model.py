import time

from sqlalchemy import BigInteger, Column, Integer, String

from src.main.repository.config import Base


class SupplierDB(Base):
    __tablename__ = "supplier"

    id = Column(Integer, primary_key=True, nullable=False, autoincrement="auto")
    customer = Column(Integer, nullable=False)
    name = Column(String, nullable=False)
    color = Column(String, nullable=False)
    created_at = Column(BigInteger, default=time.time)
    modified_at = Column(BigInteger, default=time.time, onupdate=time.time)

    def __repr__(self) -> str:
        return f"SupplierDB({self.id})"
