import math

from sqlalchemy.ext.asyncio import AsyncSession

from src.main.dto.basic_schemas import PageResponse
from src.main.dto.seller_dto import Seller
from src.main.repository.config import commit_rollback
from src.main.repository.seller_repository import SellerRepository


class SellerService:
    def __init__(self, session: AsyncSession, customer: str) -> None:
        self.session = session
        self.customer = customer
        self.page_size = 100

    async def get_all_sellers(self, page) -> PageResponse[Seller]:
        total = await SellerRepository.get_all_count(self.session, self.customer)
        result = await SellerRepository.get_all(
            self.session, self.customer, (page - 1) * self.page_size, self.page_size
        )
        response = [Seller.model_validate(seller, from_attributes=True) for seller in result]
        await commit_rollback(self.session)
        return PageResponse(
            page_number=page,
            page_size=self.page_size,
            total_pages=math.ceil(total / self.page_size),
            total_record=total,
            content=response,
        )
