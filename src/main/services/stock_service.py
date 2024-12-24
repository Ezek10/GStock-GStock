import math

from sqlalchemy.ext.asyncio import AsyncSession

from src.main.dto.basic_schemas import PageResponse
from src.main.dto.stock_dto import ResponseStock, UpdateStock
from src.main.exceptions.already_sold_error import ItemNotAvailableError
from src.main.repository.config import commit_rollback
from src.main.repository.model.stock_model import StockDB
from src.main.repository.stock_repository import StockRepository


class StockService:
    def __init__(self, session: AsyncSession, customer: str) -> None:
        self.session = session
        self.customer = customer
        self.page_size = 100

    async def update_stock(self, update_from: UpdateStock) -> None:
        stock_exist = await StockRepository.exist(self.session, update_from.id, self.customer)
        if not stock_exist:
            raise ItemNotAvailableError()
        values_to_update = {
            **update_from.model_dump(include=set(StockDB.__table__.columns.keys())),
            "customer": self.customer,
        }
        await StockRepository.update(self.session, values_to_update)
        await commit_rollback(self.session)

    async def get_all_stocks(self, page) -> PageResponse[ResponseStock]:
        total = await StockRepository.get_all_count(self.session, self.customer)
        stocks = await StockRepository.get_all(self.session, self.customer, (page - 1) * self.page_size, self.page_size)
        response = [ResponseStock.model_validate(stock, from_attributes=True) for stock in stocks]
        await commit_rollback(self.session)
        return PageResponse(
            page_number=page,
            page_size=self.page_size,
            total_pages=math.ceil(total / self.page_size),
            total_record=total,
            content=response,
        )
