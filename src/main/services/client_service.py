import math

from sqlalchemy.ext.asyncio import AsyncSession

from src.main.dto.basic_schemas import PageResponse
from src.main.dto.client_dto import Client
from src.main.repository.client_repository import ClientRepository
from src.main.repository.config import commit_rollback


class ClientService:
    def __init__(self, session: AsyncSession, customer: str) -> None:
        self.session = session
        self.customer = customer
        self.page_size = 100

    async def get_all_clients(self, page) -> PageResponse[Client]:
        total = await ClientRepository.get_all_count(self.session, self.customer)
        result = await ClientRepository.get_all(
            self.session, self.customer, (page - 1) * self.page_size, self.page_size
        )
        response = [Client.model_validate(client, from_attributes=True) for client in result]
        await commit_rollback(self.session)
        return PageResponse(
            page_number=page,
            page_size=self.page_size,
            total_pages=math.ceil(total / self.page_size),
            total_record=total,
            content=response,
        )
