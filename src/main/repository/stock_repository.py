from sqlalchemy import delete, func, update
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.sql import select

from src.main.repository.model.stock_model import StockDB


class StockRepository:
    @staticmethod
    async def create_many(session: AsyncSession, create_from: StockDB, amount: int) -> None:
        """create stock data"""
        for _ in range(amount):
            session.add(
                StockDB(
                    buy_price=create_from.buy_price,
                    product_id=create_from.product_id,
                    customer=create_from.customer,
                    buy_transaction_id=create_from.buy_transaction_id,
                    state=create_from.state,
                )
            )
        await session.flush()

    @staticmethod
    async def create(session: AsyncSession, create_from: StockDB) -> None:
        """create stock data"""
        create_from.id = None
        session.add(create_from)
        await session.flush()

    @staticmethod
    async def exist(session: AsyncSession, stock_id: int, customer: str) -> bool:
        query = select(StockDB.id).where(
            StockDB.id == stock_id, StockDB.customer == customer, StockDB.sell_transaction_id == None
        )
        stock_id = (await session.execute(query)).one_or_none()
        return bool(stock_id)

    @staticmethod
    async def delete_with_buy_id(session: AsyncSession, buy_id: int, customer: str) -> None:
        query = delete(StockDB).where(StockDB.customer == customer, StockDB.buy_transaction_id == buy_id)
        await session.execute(query)

    @staticmethod
    async def remove_sell_with_sell_id(session: AsyncSession, sell_id: int, customer: str) -> None:
        query = (
            update(StockDB)
            .where(StockDB.customer == customer, StockDB.sell_transaction_id == sell_id)
            .values({"sell_transaction_id": None})
        )
        await session.execute(query)

    @staticmethod
    async def update(session: AsyncSession, update_from: dict) -> None:
        query = (
            update(StockDB)
            .where(StockDB.id == update_from["id"], StockDB.customer == update_from["customer"])
            .values(**update_from)
        )
        await session.execute(query)

    @staticmethod
    async def update_many(session: AsyncSession, update_from: list[dict]) -> None:
        for item in update_from:
            query = update(StockDB).where(StockDB.id == item["id"], StockDB.customer == item["customer"]).values(**item)
            await session.execute(query)

    @staticmethod
    async def check_sell_transaction_ids(session: AsyncSession, products: list[dict]) -> bool:
        ids = [x["id"] for x in products]
        query = select(func.count(1)).where(StockDB.id.in_(ids), StockDB.sell_transaction_id == None)
        count = await session.scalar(query)
        return count == len(products)

    @staticmethod
    async def get_all(session: AsyncSession, customer: str, offset: int, limit: int) -> list[StockDB]:
        query = select(StockDB).where(StockDB.customer == customer, StockDB.sell_transaction_id == None)
        query = query.offset(offset).limit(limit)
        return (await session.scalars(query)).fetchall()

    @staticmethod
    async def get_all_count(session: AsyncSession, customer: str) -> int:
        query = select(StockDB).where(StockDB.customer == customer, StockDB.sell_transaction_id == None)
        count_query = select(func.count(1)).select_from(query)
        return await session.scalar(count_query)
