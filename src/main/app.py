from contextlib import asynccontextmanager
from fastapi import FastAPI, Request, Response
from fastapi.responses import JSONResponse

from src.main.authorization.admin import is_customer_verified
from src.main.controller.stock_controller import router as stock_router
from src.main.controller.client_controller import router as client_router
from src.main.controller.product_controller import router as product_router
from src.main.controller.transaction_controller import router as transaction_router
from src.main.controller.supplier_controller import router as supplier_router
from src.main.exceptions.handler import ProcessException
from src.main.repository.config import connection


async def start_up():
    connection.init()
    await connection.create_all()


async def shutdown():
    await connection.close()


@asynccontextmanager
async def lifespan(app: FastAPI):
    await start_up()
    yield
    await shutdown()


app = FastAPI(lifespan=lifespan)
app.include_router(stock_router)
app.include_router(product_router)
app.include_router(client_router)
app.include_router(supplier_router)
app.include_router(transaction_router)


exclude_paths = ["/docs", "/openapi.json"]


@app.middleware("http")
async def oauth2_authorization(request: Request, call_next):
    request.state.customer = request.headers.get("customer")
    if request.url.path in exclude_paths or is_customer_verified(
        request.state.customer
    ):
        return await call_next(request)
    return JSONResponse(content="Unauthorized", status_code=403)


@app.exception_handler(Exception)
def exception_handler(request: Request, exception: Exception) -> JSONResponse:
    """Exception Handler for all the app"""
    return ProcessException(request, exception)


@app.get("/status")
async def status() -> Response:
    return Response(content="Status: OK", status_code=200)
