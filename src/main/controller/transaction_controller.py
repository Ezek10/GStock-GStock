from fastapi import Depends, Request
from fastapi.routing import APIRouter
from sqlalchemy.ext.asyncio import AsyncSession

from src.main.dto.basic_schemas import PageResponse, ResponseSchema
from src.main.dto.transaction_dto import (
    BuyTransaction,
    Cards,
    FilterSchema,
    ResponseTransaction,
    SellTransaction,
    UpdateBuyTransaction,
    UpdateSellTransaction,
)
from src.main.repository.config import get_db_session
from src.main.services.transaction_service import TransactionService

router = APIRouter(prefix="/transaction", tags=["transaction"])


@router.post("/buy", response_model=ResponseSchema)
async def create_buy_transaction(
    request: Request,
    create_from: BuyTransaction,
    session: AsyncSession = Depends(get_db_session),
):
    result = await TransactionService(session, request.state.customer).create_buy_transaction(create_from)
    return ResponseSchema(detail="Successfully created data !", result=result)


@router.post("/sell", response_model=ResponseSchema)
async def create_sell_transaction(
    request: Request,
    create_from: SellTransaction,
    session: AsyncSession = Depends(get_db_session),
):
    result = await TransactionService(session, request.state.customer).create_sell_transaction(create_from)
    return ResponseSchema(detail="Successfully created data !", result=result)


@router.put("/buy", response_model=ResponseSchema)
async def update_buy_transactions(
    request: Request,
    update_from: UpdateBuyTransaction,
    session: AsyncSession = Depends(get_db_session),
):
    result = await TransactionService(session, request.state.customer).update_buy_transaction(update_from)
    return ResponseSchema(detail="Successfully updated data !", result=result)


@router.put("/sell", response_model=ResponseSchema)
async def update_sell_transactions(
    request: Request,
    update_from: UpdateSellTransaction,
    session: AsyncSession = Depends(get_db_session),
):
    result = await TransactionService(session, request.state.customer).update_sell_transaction(update_from)
    return ResponseSchema(detail="Successfully updated data !", result=result)


@router.delete("", response_model=ResponseSchema)
async def delete_transactions(
    request: Request,
    transaction_id: int,
    session: AsyncSession = Depends(get_db_session),
):
    result = await TransactionService(session, request.state.customer).delete_transaction(transaction_id)
    return ResponseSchema(detail="Successfully deleted transaction !", result=result)


@router.get(
    "",
    response_model=ResponseSchema[PageResponse[ResponseTransaction]],
)
async def get_all_transactions(
    request: Request,
    filters: FilterSchema = Depends(FilterSchema),
    session: AsyncSession = Depends(get_db_session),
):
    result = await TransactionService(session, request.state.customer).get_all_transactions(filters)
    return ResponseSchema(detail="Successfully fetch all transaction!", result=result)


@router.get(
    "/cards",
    response_model=ResponseSchema[Cards],
)
async def get_cards(
    request: Request,
    filters: FilterSchema = Depends(FilterSchema),
    session: AsyncSession = Depends(get_db_session),
):
    result = await TransactionService(session, request.state.customer).get_cards(filters)
    return ResponseSchema(detail="Successfully fetch transaction data by id !", result=result)
