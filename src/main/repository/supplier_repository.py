from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from src.main.repository.model.supplier_model import SupplierDB


class SupplierRepository:
    @staticmethod
    async def insert(session: AsyncSession, supplier: SupplierDB) -> SupplierDB:
        query = select(SupplierDB).where(SupplierDB.customer == supplier.customer, SupplierDB.name == supplier.name)
        supplier_db = (await session.execute(query)).scalar_one_or_none()
        if not supplier_db:
            supplier.id = None
            session.add(supplier)
            await session.flush()
        return supplier_db or supplier

    @staticmethod
    async def get_all(session: AsyncSession, customer: str, offset: int, limit: int) -> list[SupplierDB]:
        query = select(SupplierDB).where(SupplierDB.customer == customer)
        query = query.offset(offset).limit(limit)
        return (await session.scalars(query)).fetchall()

    @staticmethod
    async def get_all_count(session: AsyncSession, customer: str) -> int:
        query = select(SupplierDB).where(SupplierDB.customer == customer)
        count_query = select(func.count(1)).select_from(query)
        return await session.scalar(count_query)
