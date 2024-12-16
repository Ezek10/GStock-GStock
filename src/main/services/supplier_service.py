import math

from sqlalchemy.ext.asyncio import AsyncSession

from src.main.dto.basic_schemas import PageResponse
from src.main.dto.supplier_dto import Supplier
from src.main.repository.config import commit_rollback
from src.main.repository.supplier_repository import SupplierRepository


class SupplierService:
    def __init__(self, session: AsyncSession, customer: str) -> None:
        self.session = session
        self.customer = customer
        self.page_size = 100

    async def get_all_suppliers(self, page) -> PageResponse[Supplier]:
        total = await SupplierRepository.get_all_count(self.session, self.customer)
        result = await SupplierRepository.get_all(
            self.session, self.customer, (page - 1) * self.page_size, self.page_size
        )
        response = [Supplier.model_validate(supplier, from_attributes=True) for supplier in result]
        await commit_rollback(self.session)
        return PageResponse(
            page_number=page,
            page_size=self.page_size,
            total_pages=math.ceil(total / self.page_size),
            total_record=total,
            content=response,
        )
