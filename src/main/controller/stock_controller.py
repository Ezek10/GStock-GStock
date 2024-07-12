from fastapi import Depends, Request
from fastapi.routing import APIRouter
from sqlalchemy.ext.asyncio import AsyncSession

from src.main.dto.stock_dto import ResponseStock, UpdateStock
from src.main.dto.basic_schemas import PageResponse, ResponseSchema
from src.main.repository.config import get_db_session
from src.main.services.stock_service import StockService

router = APIRouter(prefix="/stock", tags=["stock"])


@router.put("", response_model=ResponseSchema)
async def update_stocks(
    request: Request,
    update_from: UpdateStock,
    session: AsyncSession = Depends(get_db_session),
):
    result = await StockService(session, request.state.customer).update_stock(update_from)
    return ResponseSchema(detail="Successfully updated data !", result=result)


@router.get(
    "",
    response_model=ResponseSchema[PageResponse[ResponseStock]],
)
async def get_all_stocks(
    request: Request,
    page: int = 1,
    session: AsyncSession = Depends(get_db_session),
):
    result = await StockService(session, request.state.customer).get_all_stocks(page)
    return ResponseSchema(detail="Successfully fetch stock data by id !", result=result)
