from sqlalchemy import Select, delete, distinct, func, update
from sqlalchemy.sql import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.main.dto.transaction_dto import FilterSchema, TransactionTypes
from src.main.repository.model.stock_model import StockDB
from src.main.repository.model.transaction_model import TransactionDB


def add_filters(query: Select, filters: FilterSchema) -> Select:
    if filters.filter_by_client:
        query = query.where(TransactionDB.client_id == filters.filter_by_client)
    if filters.filter_by_supplier:
        query = query.where(TransactionDB.supplier_id == filters.filter_by_supplier)
    if filters.filter_by_seller:
        query = query.where(TransactionDB.seller_id == filters.filter_by_seller)
    if filters.filter_by_specific_date:
        query = query.where(TransactionDB.date == filters.filter_by_specific_date)
    if filters.filter_by_end_date:
        query = query.where(TransactionDB.date <= filters.filter_by_end_date)
    if filters.filter_by_start_date:
        query = query.where(TransactionDB.date >= filters.filter_by_start_date)
    if filters.filter_by_buy_type:
        query = query.where(TransactionDB.type == TransactionTypes.BUY)
    if filters.filter_by_sell_type:
        query = query.where(TransactionDB.type == TransactionTypes.SELL)
    if filters.filter_by_product:
        query = query.join(StockDB, TransactionDB.id.in_([StockDB.buy_transaction_id, StockDB.sell_transaction_id]))
        query = query.where(StockDB.product_id == filters.filter_by_product)
    return query


class TransactionRepository:

    @staticmethod
    async def create(session: AsyncSession, create_from: TransactionDB) -> TransactionDB:
        """create transaction data"""
        session.add(create_from)
        await session.flush()
        return create_from

    @staticmethod
    async def delete(session: AsyncSession, transaction_id: int, customer: str):
        """delete transaction data by id"""
        query = delete(TransactionDB).where(TransactionDB.id == transaction_id, TransactionDB.customer == customer)
        await session.execute(query)
        return

    @staticmethod
    async def exist(session: AsyncSession, id: int, customer):
        query = select(TransactionDB.id).where(TransactionDB.id == id, TransactionDB.customer == customer)
        id = (await session.execute(query)).one_or_none()
        return True if id else False

    @staticmethod
    async def update(session: AsyncSession, update_from: dict):
        query = (
            update(TransactionDB).
            where(TransactionDB.id == update_from["id"], TransactionDB.customer == update_from["customer"])
            .values(**update_from)
        )
        await session.execute(query)
        return

    @staticmethod
    async def get_all(
        session: AsyncSession, customer: str, offset: int, limit: int, filters: FilterSchema
    ) -> list[TransactionDB]:
        query = select(TransactionDB).distinct(TransactionDB.id).where(TransactionDB.customer == customer)
        query = add_filters(query, filters)
        query = query.offset(offset).limit(limit).order_by(TransactionDB.created_at.desc())
        result = (await session.scalars(query)).fetchall()
        return result


    @staticmethod
    async def get_all_count(session: AsyncSession, customer: str, filters: FilterSchema) -> int:
        query = select(func.count(distinct(TransactionDB.id))).where(TransactionDB.customer == customer)
        query = add_filters(query, filters)
        total_record = await session.scalar(query)
        return total_record
