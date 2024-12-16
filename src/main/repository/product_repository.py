from sqlalchemy import func, select, update
from sqlalchemy.ext.asyncio import AsyncSession

from src.main.repository.model.product_model import ProductDB


class ProductRepository:
    @staticmethod
    async def insert(session: AsyncSession, product: ProductDB) -> ProductDB:
        query = select(ProductDB).where(ProductDB.customer == product.customer, ProductDB.name == product.name)
        product_db = (await session.execute(query)).scalar_one_or_none()
        if not product_db:
            product.id = None
            session.add(product)
            await session.flush()
        elif product_db.is_active is False:
            product_db.is_active = True
        return product_db or product

    @staticmethod
    async def get_all(session: AsyncSession, customer: str, offset: int, limit: int) -> list[ProductDB]:
        query = select(ProductDB).where(ProductDB.customer == customer, ProductDB.is_active is True)
        query = query.order_by(ProductDB.name)
        query = query.offset(offset).limit(limit)
        result = (await session.scalars(query)).fetchall()
        return list(result)

    @staticmethod
    async def get(session: AsyncSession, product_id: int, customer: str) -> ProductDB:
        query = select(ProductDB).where(
            ProductDB.customer == customer, ProductDB.id == product_id, ProductDB.is_active is True
        )
        return (await session.scalars(query)).one_or_none()

    @staticmethod
    async def delete(session: AsyncSession, product_id: int, customer: str) -> None:
        # Products are not deleted they get disabled
        query = (
            update(ProductDB)
            .where(ProductDB.customer == customer, ProductDB.id == product_id)
            .values({"is_active": False})
        )
        await session.execute(query)

    @staticmethod
    async def get_all_count(session: AsyncSession, customer: str) -> int:
        query = select(ProductDB).where(ProductDB.customer == customer, ProductDB.is_active is True)
        count_query = select(func.count(1)).select_from(query)
        return await session.scalar(count_query)

    @staticmethod
    async def exist(session: AsyncSession, product_id: int, customer) -> bool:
        query = select(ProductDB.id).where(ProductDB.id == product_id, ProductDB.customer == customer)
        product_id = (await session.execute(query)).one_or_none()
        return bool(product_id)

    @staticmethod
    async def update(session: AsyncSession, update_from: dict) -> None:
        query = (
            update(ProductDB)
            .where(ProductDB.id == update_from["id"], ProductDB.customer == update_from["customer"])
            .values(**update_from)
        )
        await session.execute(query)
