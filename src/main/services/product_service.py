import math

from sqlalchemy.ext.asyncio import AsyncSession

from src.main.dto.basic_schemas import PageResponse
from src.main.dto.product_dto import Product, ProductStock, UpdateProduct
from src.main.exceptions.already_sold_error import ItemNotAvailableError
from src.main.repository.config import commit_rollback
from src.main.repository.model.product_model import ProductDB
from src.main.repository.product_repository import ProductRepository


class ProductService:
    def __init__(self, session: AsyncSession, customer: str) -> None:
        self.session = session
        self.customer = customer
        self.page_size = 100

    async def delete_product(self, product_id) -> None:
        await ProductRepository.delete(self.session, product_id, self.customer)
        await commit_rollback(self.session)

    async def update_product(self, update_from: UpdateProduct) -> None:
        product_exist = await ProductRepository.exist(self.session, update_from.id, self.customer)
        if not product_exist:
            raise ItemNotAvailableError()
        values_to_update = {
            **update_from.model_dump(include=set(ProductDB.__table__.columns.keys())),
            "customer": self.customer,
        }
        await ProductRepository.update(self.session, values_to_update)
        await commit_rollback(self.session)

    async def get_all_products(self, page) -> PageResponse[Product]:
        total = await ProductRepository.get_all_count(self.session, self.customer)
        result = await ProductRepository.get_all(
            self.session, self.customer, (page - 1) * self.page_size, self.page_size
        )
        response = [Product.model_validate(product, from_attributes=True) for product in result]
        await commit_rollback(self.session)
        return PageResponse(
            page_number=page,
            page_size=self.page_size,
            total_pages=math.ceil(total / self.page_size),
            total_record=total,
            content=response,
        )

    async def get_all_products_stocks(self, page) -> PageResponse[ProductStock]:
        total = await ProductRepository.get_all_count(self.session, self.customer)
        result = await ProductRepository.get_all(
            self.session, self.customer, (page - 1) * self.page_size, self.page_size
        )
        response = [ProductStock.model_validate(product, from_attributes=True) for product in result]

        warning_low_stock = 3

        def is_data_missing(stock) -> bool:
            return not bool(stock.serial_id)

        for product in response:
            product.warning_stock = len(product.stocks) < warning_low_stock
            for stock in product.stocks:
                stock.missing_data = is_data_missing(stock)
        await commit_rollback(self.session)
        return PageResponse(
            page_number=page,
            page_size=self.page_size,
            total_pages=math.ceil(total / self.page_size),
            total_record=total,
            content=response,
        )
