import os

from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from src.main.exceptions.already_exist_error import AlreadyExistError

Base = declarative_base()


class AsyncDatabaseSession(AsyncSession):
    def __init__(self) -> None:
        self.session = None
        self.engine = None

    def __getattr__(self, name):
        return getattr(self.session, name)

    def init(self) -> None:
        db_engine = os.environ["DB_ENGINE"]
        db_username = os.environ["DB_USERNAME"]
        db_password = os.environ["DB_PASSWORD"]
        db_host = os.environ["DB_HOST"]
        db_port = os.environ["DB_PORT"]
        db_name = os.environ["DB_GSTOCK"]
        db_config = f"{db_engine}://{db_username}:{db_password}@{db_host}:{db_port}/{db_name}"
        self.engine = create_async_engine(db_config, future=True, echo=True, pool_size=10, max_overflow=20)
        self.session_maker = sessionmaker(self.engine, expire_on_commit=False, class_=AsyncSession)

    async def create_all(self) -> None:
        async with self.engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)


connection = AsyncDatabaseSession()


async def get_db_session():
    session = connection.session_maker()
    try:
        yield session
    finally:
        await session.close()


async def commit_rollback(session: AsyncSession) -> None:
    """
    Commit funcion with rollback if raises in commit
    raises AlreadyExist Exception if Integrity Error is thrown
    """
    try:
        await session.commit()
    except IntegrityError as ex:
        await session.rollback()
        raise AlreadyExistError from ex
    except Exception:
        await session.rollback()
        raise
