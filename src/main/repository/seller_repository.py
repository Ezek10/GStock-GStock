from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from src.main.repository.model.seller_model import SellerDB


class SellerRepository:
    @staticmethod
    async def insert(session: AsyncSession, seller: SellerDB) -> SellerDB:
        query = select(SellerDB).where(SellerDB.customer == seller.customer, SellerDB.name == seller.name)
        seller_db = (await session.execute(query)).scalar_one_or_none()
        if not seller_db:
            # insert in table
            seller.id = None
            session.add(seller)
            await session.flush()
        else:
            # update values
            seller_db.email = seller.email
            seller_db.cellphone = seller.cellphone
        return seller_db or seller

    @staticmethod
    async def get_all(session: AsyncSession, customer: str, offset: int, limit: int) -> list[SellerDB]:
        query = select(SellerDB).where(SellerDB.customer == customer)
        query = query.offset(offset).limit(limit)
        return (await session.scalars(query)).fetchall()

    @staticmethod
    async def get_all_count(session: AsyncSession, customer: str) -> int:
        query = select(SellerDB).where(SellerDB.customer == customer)
        count_query = select(func.count(1)).select_from(query)
        return await session.scalar(count_query)
