import math
from sqlalchemy.ext.asyncio import AsyncSession

from src.main.dto.transaction_dto import (
    BuyTransaction,
    Cards,
    ContactVias,
    FilterSchema,
    ResponseTransaction,
    SellTransaction,
    TransactionTypes,
    UpdateBuyTransaction,
    UpdateSellTransaction
)
from src.main.dto.basic_schemas import PageResponse
from src.main.exceptions.already_sold_exception import ItemNotAvailableException
from src.main.repository.client_repository import ClientRepository
from src.main.repository.config import commit_rollback
from src.main.repository.model.client_model import ClientDB
from src.main.repository.model.product_model import ProductDB
from src.main.repository.model.seller_model import SellerDB
from src.main.repository.model.stock_model import StockDB
from src.main.repository.model.supplier_model import SupplierDB
from src.main.repository.model.transaction_model import TransactionDB
from src.main.repository.product_repository import ProductRepository
from src.main.repository.seller_repository import SellerRepository
from src.main.repository.stock_repository import StockRepository
from src.main.repository.transaction_repository import TransactionRepository
from src.main.repository.supplier_repository import SupplierRepository


class TransactionService:
    def __init__(self, session: AsyncSession, customer: str) -> None:
        self.session = session
        self.customer = customer
        self.page_size = 10000

    async def create_buy_transaction(self, create_from: BuyTransaction):

        supplier = SupplierDB(
            **create_from.supplier.model_dump(include=set(SupplierDB.__table__.columns.keys())),
            customer=self.customer
        )
        supplier = await SupplierRepository.insert(
            self.session,
            supplier
        )
        transaction = TransactionDB(
            **create_from.model_dump(include=set(TransactionDB.__table__.columns.keys())),
            customer=self.customer,
            supplier_id=supplier.id,
        )
        transaction = await TransactionRepository.create(self.session, transaction)

        for product_to_create in create_from.products:
            product = ProductDB(customer=self.customer, name=product_to_create.product_name)
            product = await ProductRepository.insert(self.session, product)
            stock_db = StockDB(
                **product_to_create.model_dump(include=set(StockDB.__table__.columns.keys())),
                customer=self.customer,
                product_id = product.id,
                buy_transaction_id = transaction.id
            )
            await StockRepository.create(self.session, stock_db)

        await commit_rollback(self.session)
        return

    async def create_sell_transaction(self, create_from: SellTransaction):
        # Contact via lo debe enviar nico desde front sabiendo la lista de clientes que ya existe
        # Preguntar a nico si el deberia enviarme 
        client = ClientDB(
            **create_from.client.model_dump(include=set(ClientDB.__table__.columns.keys())),
            customer=self.customer
        )
        client = await ClientRepository.insert(self.session, client)
        seller = SellerDB(
            **create_from.seller.model_dump(include=set(SellerDB.__table__.columns.keys())),
            customer=self.customer
        )
        seller = await SellerRepository.insert(self.session, seller)
        if create_from.has_swap:
            supplier = await SupplierRepository.insert(self.session, SupplierDB(customer=self.customer, name="SWAP", color="#808080"))
        transaction = TransactionDB(
            **create_from.model_dump(include=set(TransactionDB.__table__.columns.keys())),
            client_id=client.id,
            seller_id=seller.id,
            customer=self.customer,
            supplier_id=supplier.id if create_from.has_swap else None,
        )
        transaction = await TransactionRepository.create(self.session, transaction)
        products = [
            {
                "sell_price": prd.sell_price, 
                "id": prd.id, 
                "customer": self.customer, 
                "sell_transaction_id": transaction.id
            } for prd in create_from.products
        ]
        if not await StockRepository.check_sell_transaction_ids(self.session, products):
            raise ItemNotAvailableException()
        await StockRepository.update_many(self.session, products)

        if create_from.has_swap:
            for swap_item in create_from.swap_products:
                product = ProductDB(customer=self.customer, name=swap_item.product_name)
                product = await ProductRepository.insert(self.session, product)
                swap_item_to_create = StockDB(
                    **swap_item.model_dump(include=set(StockDB.__table__.columns.keys())),
                    customer=self.customer,
                    product_id=product.id,
                    buy_transaction_id=transaction.id
                )
                await StockRepository.create(self.session, swap_item_to_create)

        await commit_rollback(self.session)
        return

    async def update_buy_transaction(self, update_from: UpdateBuyTransaction):
        transaction_exist = await TransactionRepository.exist(self.session, update_from.id, self.customer)
        if not transaction_exist:
            raise ItemNotAvailableException()
        supplier = SupplierDB(
            **update_from.supplier.model_dump(include=set(SupplierDB.__table__.columns.keys())),
            customer=self.customer
        )
        supplier = await SupplierRepository.insert(
            self.session,
            supplier
        )
        transaction_values_to_update = {
            **update_from.model_dump(include=set(TransactionDB.__table__.columns.keys())),
            "supplier_id": supplier.id,
            "customer":self.customer
        }
        await TransactionRepository.update(self.session, transaction_values_to_update)
        for product_to_update in update_from.products:
            product = ProductDB(customer=self.customer, name=product_to_update.product_name)
            product = await ProductRepository.insert(self.session, product)
            await StockRepository.delete_with_buy_id(self.session, update_from.id, self.customer)
            stock_db = StockDB(
                **product_to_update.model_dump(include=set(StockDB.__table__.columns.keys())),
                customer=self.customer,
                product_id = product.id,
                buy_transaction_id = update_from.id
            )
            await StockRepository.create(self.session, stock_db)
        await commit_rollback(self.session)
        return

    async def update_sell_transaction(self, update_from: UpdateSellTransaction):
        transaction_exist = await TransactionRepository.exist(self.session, update_from.id, self.customer)
        if not transaction_exist:
            raise ItemNotAvailableException()
        client = ClientDB(
            **update_from.client.model_dump(include=set(ClientDB.__table__.columns.keys())),
            customer=self.customer
        )
        client = await ClientRepository.insert(self.session, client)
        seller = SellerDB(
            **update_from.seller.model_dump(include=set(SellerDB.__table__.columns.keys())),
            customer=self.customer
        )
        seller = await SellerRepository.insert(self.session, seller)
        if update_from.has_swap:
            supplier = await SupplierRepository.insert(self.session, SupplierDB(customer=self.customer, name="SWAP", color="#808080"))
        transaction_values_to_update = {
            **update_from.model_dump(include=set(TransactionDB.__table__.columns.keys())),
            "client_id": client.id,
            "customer": self.customer,
            "supplier_id": supplier.id if update_from.has_swap else None,
            "seller_id": seller.id
        }
        await TransactionRepository.update(self.session, transaction_values_to_update)
        await StockRepository.remove_sell_with_sell_id(self.session, update_from.id, self.customer)
        await StockRepository.delete_with_buy_id(self.session, update_from.id, self.customer)
        products = [
            {
                "sell_price": prd.sell_price, 
                "id": prd.id, 
                "customer": self.customer, 
                "sell_transaction_id": update_from.id
            } for prd in update_from.products
        ]
        if not await StockRepository.check_sell_transaction_ids(self.session, products):
            raise ItemNotAvailableException()
        await StockRepository.update_many(self.session, products)
        if update_from.has_swap:
            for swap_item in update_from.swap_products:
                product = ProductDB(customer=self.customer, name=swap_item.product_name)
                product = await ProductRepository.insert(self.session, product)
                swap_item_to_create = StockDB(
                    **swap_item.model_dump(include=set(StockDB.__table__.columns.keys())),
                    customer=self.customer,
                    product_id = product.id,
                    buy_transaction_id = update_from.id
                )
                await StockRepository.create(self.session, swap_item_to_create)
        await commit_rollback(self.session)
        return

    async def get_all_transactions(self, filters: FilterSchema) -> PageResponse[ResponseTransaction]:
        total_count = await TransactionRepository.get_all_count(self.session, self.customer, filters)
        transactions = await TransactionRepository.get_all(
            self.session, self.customer, (filters.page-1)*self.page_size, self.page_size, filters
        )
        transactions_response = []
        for transaction in transactions:
            transaction_products = transaction.buy_stocks if transaction.type == TransactionTypes.BUY else transaction.sell_stocks
            transaction_price = 0
            name = transaction.supplier.name if transaction.type == TransactionTypes.BUY else transaction.client.name
            for product in transaction_products:
                transaction_price += product.buy_price if transaction.type == TransactionTypes.BUY else product.sell_price
            if transaction.has_swap:
                for swap_product in transaction.buy_stocks:
                    transaction_price -= swap_product.buy_price
            transactions_response.append(
                ResponseTransaction(
                    id=transaction.id,
                    name=name,
                    seller=transaction.seller,
                    total=transaction_price,
                    type=transaction.type,
                    payment_method=transaction.payment_method,
                    date=transaction.date,
                    contact_via=transaction.contact_via,
                    products=transaction_products,
                    swap_products=transaction.buy_stocks if transaction.has_swap else [],
                    supplier=transaction.supplier if transaction.supplier else None,
                    client=transaction.client if transaction.client else None
                )
            )
        transactions_response = sorted(transactions_response, key=lambda x: x.date, reverse=True)
        await commit_rollback(self.session)
        return PageResponse(
            page_number=filters.page,
            page_size=self.page_size,
            total_pages=math.ceil(total_count/self.page_size), 
            total_record=total_count,
            content=transactions_response
        )

    async def get_cards(self, filters: FilterSchema) -> Cards:
        transactions = await TransactionRepository.get_all(
            self.session, self.customer, 0, 999999, filters
        )

        sell_channels = {name: 0 for name in ContactVias._member_names_}
        sell_transactions = list(filter(lambda x: x.type == TransactionTypes.SELL, transactions))
        if len(sell_transactions):
            for k in sell_channels.keys():
                sell_channels[k] = len(list(filter(lambda x: x.contact_via == k, sell_transactions)))/len(sell_transactions)*100

        product_bought = 0
        for transaction in transactions:
            product_bought += len(transaction.buy_stocks)

        product_sold = 0
        for transaction in sell_transactions:
            product_sold += len(transaction.sell_stocks)

        earns = 0
        for transaction in transactions:
            for stock in transaction.sell_stocks:
                earns += stock.sell_price - stock.buy_price

        sellers = {transaction.seller.name: 0 for transaction in transactions if transaction.seller}
        for transaction in transactions:
            if transaction.seller:
                sellers[transaction.seller.name] += len(transaction.sell_stocks)
        sellers = sorted(sellers.items(), key=lambda x: x[1], reverse=True)
        sellers = sellers[:6]
        sellers = {s[0]: s[1] for s in sellers}

        return Cards(
            channels=sell_channels,
            product_bought=product_bought,
            product_sold=product_sold,
            earns=earns,
            sellers=sellers
        )

    async def delete_transaction(self, transaction_id: int):
        await StockRepository.remove_sell_with_sell_id(self.session, transaction_id, self.customer)
        await StockRepository.delete_with_buy_id(self.session, transaction_id, self.customer)
        await TransactionRepository.delete(self.session, transaction_id, self.customer)
        await commit_rollback(self.session)
        return
