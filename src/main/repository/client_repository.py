from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from src.main.repository.model.client_model import ClientDB


class ClientRepository:
    @staticmethod
    async def insert(session: AsyncSession, client: ClientDB) -> ClientDB:
        query = select(ClientDB).where(ClientDB.customer == client.customer, ClientDB.name == client.name)
        client_db = (await session.execute(query)).scalar_one_or_none()
        if not client_db:
            # insert in table
            client.id = None
            session.add(client)
            await session.flush()
        else:
            # update values
            client_db.email = client.email
            client_db.cellphone = client.cellphone
        return client_db or client

    @staticmethod
    async def get_all(session: AsyncSession, customer: str, offset: int, limit: int) -> list[ClientDB]:
        query = select(ClientDB).where(ClientDB.customer == customer)
        query = query.offset(offset).limit(limit)
        return (await session.scalars(query)).fetchall()

    @staticmethod
    async def get_all_count(session: AsyncSession, customer: str) -> int:
        query = select(ClientDB).where(ClientDB.customer == customer)
        count_query = select(func.count(1)).select_from(query)
        return await session.scalar(count_query)
