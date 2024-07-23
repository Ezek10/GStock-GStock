from contextlib import asynccontextmanager
import os
from fastapi import Depends, FastAPI, Request, Response
from fastapi.responses import JSONResponse

from src.main.authorization.admin import get_user_with_token
from src.main.controller.stock_controller import router as stock_router
from src.main.controller.client_controller import router as client_router
from src.main.controller.seller_controller import router as seller_router
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

APP_PREFIX = os.environ["GSTOCK_PREFIX"]

app = FastAPI(lifespan=lifespan, openapi_prefix=APP_PREFIX)
app.include_router(stock_router)
app.include_router(product_router)
app.include_router(client_router)
app.include_router(supplier_router)
app.include_router(transaction_router)
app.include_router(seller_router)

exclude_paths = [
    "/docs",
    "/openapi.json",
    "/health_check"
]

@app.middleware("http")
async def oauth2_authorization(request: Request, call_next):
    #CLEAR PATH
    path = request.url.path.replace(APP_PREFIX, "")
    if path in exclude_paths:
        return await call_next(request)
    # Enable Auth
    token = request.headers.get("Authorization", "").replace("Bearer ", "")
    #SET USER JSON ON REQUEST
    user = get_user_with_token(token, path)
    if user:
        request.state.user=user
        request.state.customer=user["customer"]
        return await call_next(request)
    else:
        return JSONResponse(content="Unauthorized", status_code=403)


@app.exception_handler(Exception)
def exception_handler(request: Request, exception: Exception) -> JSONResponse:
    """Exception Handler for all the app"""
    return ProcessException(request, exception)


@app.get("/health_check")
async def status() -> Response:
    return Response(content="Status: OK", status_code=200)
