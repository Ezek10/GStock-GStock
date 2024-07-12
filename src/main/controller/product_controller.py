from fastapi import Depends, Request
from fastapi.routing import APIRouter
from sqlalchemy.ext.asyncio import AsyncSession

from src.main.dto.product_dto import Product, ProductStock, UpdateProduct
from src.main.dto.basic_schemas import PageResponse, ResponseSchema
from src.main.repository.config import get_db_session
from src.main.services.product_service import ProductService

router = APIRouter(prefix="/product", tags=["product"])


@router.put("", response_model=ResponseSchema)
async def update_products(
    request: Request,
    update_from: UpdateProduct,
    session: AsyncSession = Depends(get_db_session),
):
    result = await ProductService(session, request.state.customer).update_product(update_from)
    return ResponseSchema(detail="Successfully updated data !", result=result)


@router.get("", response_model=ResponseSchema[PageResponse[Product]])
async def get_products(
    request: Request,
    session: AsyncSession = Depends(get_db_session),
    page: int = 1
):
    result = await ProductService(session, request.state.customer).get_all_products(page)
    return ResponseSchema(detail="Successfully updated data !", result=result)


@router.delete("", response_model=ResponseSchema)
async def delete_products(
    request: Request,
    product_id: str,
    session: AsyncSession = Depends(get_db_session),
):
    result = await ProductService(session, request.state.customer).delete_product(product_id)
    return ResponseSchema(detail="Successfully deleted data !", result=result)


@router.get("/stock", response_model=ResponseSchema[PageResponse[ProductStock]])
async def get_products_stocks(
    request: Request,
    session: AsyncSession = Depends(get_db_session),
    page: int = 1
):
    result = await ProductService(session, request.state.customer).get_all_products_stocks(page)
    return ResponseSchema(detail="Successfully updated data !", result=result)

