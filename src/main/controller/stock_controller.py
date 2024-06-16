from fastapi import Depends
from fastapi.routing import APIRouter
from src.main.authorization.admin import verify_key

from main.controller.view.stock_view import Stocks
from main.repository.stock_repository import StockRepository
from main.page_schema import PageResponse, ResponseSchema

router = APIRouter(prefix="/stocks", tags=["stock"])


@router.post("", response_model=ResponseSchema, dependencies=[Depends(verify_key)])
async def create_stocks(create_from: Stocks):
    result = await StockRepository.create(create_from)
    return ResponseSchema(detail="Successfully created data !", result=result)


@router.delete(
    "/{stock_id}", response_model=ResponseSchema, dependencies=[Depends(verify_key)]
)
async def delete_stock(stock_id: int):
    await StockRepository.delete(stock_id)
    return ResponseSchema(detail="Successfully deleted data !")


@router.get(
    "",
    response_model=ResponseSchema[PageResponse[Stocks]],
    dependencies=[Depends(verify_key)],
)
async def get_all_stocks():
    result = await StockRepository.get_all()
    return ResponseSchema(
        detail="Successfully fetch stock data by id !", result=result
    )
