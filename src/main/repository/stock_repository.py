import math

from sqlalchemy import delete, func
from sqlalchemy.sql import select

from main.controller.view.stock_view import Stocks
from src.main.repository.config import commit_rollback, db
from main.repository.model.stock_model import StockDB
from main.page_schema import PageResponse


class stockRepository:
    @staticmethod
    async def create(create_from: Stocks):
        """create stock data"""
        for stock in create_from:
            db.add(StockDB(id=stock.id, name=stock.name))
        await commit_rollback()

    @staticmethod
    async def delete(stock_id: int):
        """delete stock data by id"""

        query = delete(StockDB).where(StockDB.id == stock_id)
        await db.execute(query)
        await commit_rollback()

    @staticmethod
    async def get_all(page: int = 1, limit: int = 100) -> PageResponse[Stocks]:
        query = select(StockDB)
        count_query = select(func.count(1)).select_from(query)
        offset_page = page - 1
        query = query.offset(offset_page * limit).limit(limit)
        total_record = await db.scalar(count_query)
        total_page = math.ceil(total_record / limit)
        result = (await db.scalars(query)).fetchall()

        return PageResponse(
            page_number=page,
            page_size=limit,
            total_pages=total_page,
            total_record=total_record,
            content=Stocks.model_validate(result),
        )
