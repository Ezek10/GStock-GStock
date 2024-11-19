from sqlalchemy import delete, func, select, update
from sqlalchemy.ext.asyncio import AsyncSession

from src.main.repository.model.product_model import ProductDB


class ProductRepository:

    @staticmethod
    async def insert(session: AsyncSession, product: ProductDB) -> ProductDB:
        query = select(ProductDB).where(
            ProductDB.customer == product.customer,
            ProductDB.name == product.name
        )
        product_db = (await session.execute(query)).scalar_one_or_none()
        if not product_db:
            product.id = None
            session.add(product)
            await session.flush()
        elif product_db.is_active is False:
            product_db.is_active = True
        return product_db or product

    @staticmethod
    async def get_all(
        session: AsyncSession, customer: str, offset: int, limit: int
    ) -> list[ProductDB]:
        query = select(ProductDB).where(ProductDB.customer == customer, ProductDB.is_active == True)
        query.order_by(ProductDB.name)
        query = query.offset(offset).limit(limit)
        result = (await session.scalars(query)).fetchall()
        return list(result)

    @staticmethod
    async def get(
        session: AsyncSession, product_id: int, customer: str
    ) -> ProductDB:
        query = select(ProductDB).where(ProductDB.customer == customer, ProductDB.id == product_id, ProductDB.is_active == True)
        result = (await session.scalars(query)).one_or_none()
        return result

    @staticmethod
    async def delete(
        session: AsyncSession, product_id: int, customer: str
    ):
        # Products are not deleted they get disabled
        query = update(ProductDB).where(ProductDB.customer == customer, ProductDB.id == product_id).values({"is_active":False})
        await session.execute(query)
        return

    @staticmethod
    async def get_all_count(session: AsyncSession, customer: str) -> int:
        query = select(ProductDB).where(ProductDB.customer == customer, ProductDB.is_active == True)
        count_query = select(func.count(1)).select_from(query)
        total_record = await session.scalar(count_query)
        return total_record

    @staticmethod
    async def exist(session: AsyncSession, id: int, customer) -> bool:
        query = select(ProductDB.id).where(ProductDB.id == id, ProductDB.customer == customer)
        id = (await session.execute(query)).one_or_none()
        return True if id else False

    @staticmethod
    async def update(session: AsyncSession, update_from: dict):
        query = (
            update(ProductDB).
            where(ProductDB.id == update_from["id"], ProductDB.customer == update_from["customer"])
            .values(**update_from)
        )
        await session.execute(query)
        return
