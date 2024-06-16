import time
from sqlalchemy import BigInteger, Boolean, Column, Integer, String

from src.main.repository.config import Base


class UserDB(Base):
    __tablename__ = "user"

    id = Column(Integer, primary_key=True, nullable=False)
    customer = Column(String, nullable=False)
    name = Column(String)
    last_name = Column(String)
    email = Column(String, nullable=False)
    restart_password = Column(Boolean, default=False)
    password =Column(String, nullable=False)

    create_at = Column(BigInteger, default_factory=time.time)
    modified_at = Column(BigInteger, default=time.time, onupdate=time.time)

    def __repr__(self):
        return f"UserDB({self.id})"
