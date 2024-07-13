from fastapi import Depends, Request
from fastapi.routing import APIRouter
from sqlalchemy.ext.asyncio import AsyncSession

from src.main.dto.seller_dto import Seller
from src.main.dto.basic_schemas import PageResponse, ResponseSchema
from src.main.repository.config import get_db_session
from src.main.services.seller_service import SellerService

router = APIRouter(prefix="/seller", tags=["seller"])


@router.get("", response_model=ResponseSchema[PageResponse[Seller]])
async def get_sellers(
    request: Request,
    session: AsyncSession = Depends(get_db_session),
    page: int = 1
):
    result = await SellerService(session, request.state.customer).get_all_sellers(page)
    return ResponseSchema(detail="Successfully updated data !", result=result)
