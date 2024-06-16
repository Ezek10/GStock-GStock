import time
from sqlalchemy import BigInteger, Column, Integer, String

from src.main.repository.config import Base


class ClientDB(Base):
    __tablename__ = "client"

    id = Column(Integer, primary_key=True, nullable=False)
    customer = Column(String, nullable=False)
    name = Column(String)
    last_name = Column(String)
    email = Column(String, nullable=False)
    tel = Column(String, nullable=False)
    address = Column(String)
    document = Column(String)

    create_at = Column(BigInteger, default_factory=time.time)
    modified_at = Column(BigInteger, default=time.time, onupdate=time.time)

    def __repr__(self):
        return f"ClientDB({self.id})"
