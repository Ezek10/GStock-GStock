from fastapi import Depends, Request
from fastapi.routing import APIRouter
from sqlalchemy.ext.asyncio import AsyncSession

from src.main.dto.supplier_dto import Supplier
from src.main.dto.basic_schemas import PageResponse, ResponseSchema
from src.main.repository.config import get_db_session
from src.main.services.supplier_service import SupplierService

router = APIRouter(prefix="/supplier", tags=["supplier"])


@router.get("", response_model=ResponseSchema[PageResponse[Supplier]])
async def get_suppliers(
    request: Request,
    session: AsyncSession = Depends(get_db_session),
    page: int = 1
):
    result = await SupplierService(session, request.state.customer).get_all_suppliers(page)
    return ResponseSchema(detail="Successfully updated data !", result=result)
