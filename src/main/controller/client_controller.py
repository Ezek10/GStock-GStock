from fastapi import Depends, Request
from fastapi.routing import APIRouter
from sqlalchemy.ext.asyncio import AsyncSession

from src.main.dto.client_dto import Client
from src.main.dto.basic_schemas import PageResponse, ResponseSchema
from src.main.repository.config import get_db_session
from src.main.services.client_service import ClientService

router = APIRouter(prefix="/client", tags=["client"])


@router.get("", response_model=ResponseSchema[PageResponse[Client]])
async def get_clients(
    request: Request,
    session: AsyncSession = Depends(get_db_session),
    page: int = 1
):
    result = await ClientService(session, request.state.customer).get_all_clients(page)
    return ResponseSchema(detail="Successfully updated data !", result=result)
