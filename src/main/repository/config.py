import os
from src.main.exceptions.already_exist_exception import AlreadyExistException

from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import IntegrityError


Base = declarative_base()


class AsyncDatabaseSession(AsyncSession):
    def __init__(self):
        self.session = None
        self.engine = None

    def __getattr__(self, name):
        return getattr(self.session, name)

    def init(self):
        DB_ENGINE = os.environ["DB_ENGINE"]
        DB_USERNAME = os.environ["DB_USERNAME"]
        DB_PASSWORD = os.environ["DB_PASSWORD"]
        DB_HOST = os.environ["DB_HOST"]
        DB_PORT = os.environ["DB_PORT"]
        DB_NAME = os.environ["DB_GSTOCK"]
        DB_CONFIG = (
            f"{DB_ENGINE}://{DB_USERNAME}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
        )
        self.engine = create_async_engine(
            DB_CONFIG, future=True, echo=True, pool_size=10, max_overflow=20
        )
        self.session_maker = sessionmaker(
            self.engine, expire_on_commit=False, class_=AsyncSession
        )

    async def create_all(self):
        async with self.engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)


connection = AsyncDatabaseSession()


async def get_db_session():
    session = connection.session_maker()
    try:
        yield session
    finally:
        await session.close()


async def commit_rollback(session: AsyncSession):
    """
    Commit funcion with rollback if raises in commit
    raises AlreadyExist Exception if Integrity Error is thrown
    """
    try:
        await session.commit()
    except IntegrityError:
        await session.rollback()
        raise AlreadyExistException()
    except Exception:
        await session.rollback()
        raise
