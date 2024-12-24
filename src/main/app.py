import gzip
import os
from contextlib import asynccontextmanager

from apscheduler.schedulers.background import BackgroundScheduler  # runs tasks in the background
from apscheduler.triggers.cron import CronTrigger  # allows us to specify a recurring time for execution
from fastapi import FastAPI, Request, Response
from fastapi.responses import JSONResponse
from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
from sh import pg_dump

from src.main.authorization.admin import get_user_with_token
from src.main.controller.client_controller import router as client_router
from src.main.controller.product_controller import router as product_router
from src.main.controller.seller_controller import router as seller_router
from src.main.controller.stock_controller import router as stock_router
from src.main.controller.supplier_controller import router as supplier_router
from src.main.controller.transaction_controller import router as transaction_router
from src.main.exceptions.handler import process_exception
from src.main.repository.config import connection


# The task to run
def backup_database():
    os.environ["PGPASSWORD"] = os.environ["DB_PASSWORD"]
    with gzip.open("backup.gz", "wb") as f:
        pg_dump(
            "-h",
            os.environ["DB_HOST"],
            "-p",
            os.environ["DB_PORT"],
            "-U",
            os.environ["DB_USERNAME"],
            os.environ["DB_GSTOCK"],
            "--clean",
            "--column-inserts",
            "--if-exists",
            _out=f,
        )

    # Credenciales del servicio de cuenta
    credentials = service_account.Credentials.from_service_account_file("secret.json")

    # Servicio de Google Drive
    drive_service = build("drive", "v3", credentials=credentials)

    # Subir un archivo
    file_metadata = {
        "name": "backup.sql",
        "parents": ["folder_id"],  # ID de la carpeta de respaldo
    }
    media = MediaFileUpload("backup.sql", mimetype="application/sql")
    drive_service.files().create(body=file_metadata, media_body=media, fields="id").execute()

    # ... additional task code goes here ...


# Set up the scheduler
scheduler = BackgroundScheduler()
trigger = CronTrigger(hour=14, minute=36)
scheduler.add_job(backup_database, trigger)
scheduler.start()


async def start_up() -> None:
    connection.init()
    await connection.create_all()


async def shutdown() -> None:
    await connection.close()


@asynccontextmanager
async def lifespan(app: FastAPI):  # noqa: ARG001
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


@app.options("/{rest_of_path:path}")
async def preflight_handler() -> Response:
    response = Response()
    response.headers["Access-Control-Allow-Origin"] = "*"
    response.headers["Access-Control-Allow-Methods"] = "DELETE, GET, HEAD, OPTIONS, PATCH, POST, PUT"
    response.headers["Access-Control-Allow-Headers"] = "Authorization, Content-Type, use_cache, cache-control"
    return response


@app.middleware("http")
async def add_cors_header(request: Request, call_next):
    response = await call_next(request)
    response.headers["Access-Control-Allow-Origin"] = "*"
    response.headers["Access-Control-Allow-Methods"] = "DELETE, GET, HEAD, OPTIONS, PATCH, POST, PUT"
    response.headers["Access-Control-Allow-Headers"] = "Authorization, Content-Type, use_cache, cache-control"
    return response


exclude_paths = ["/docs", "/openapi.json", "/health_check"]


@app.middleware("http")
async def oauth2_authorization(request: Request, call_next):
    # CLEAR PATH
    path = request.url.path.replace(APP_PREFIX, "")
    if path in exclude_paths or request.method == "OPTIONS":
        return await call_next(request)
    # Enable Auth
    token = request.headers.get("Authorization", "").replace("Bearer ", "")
    # SET USER JSON ON REQUEST
    user = get_user_with_token(token)
    request.state.user = user
    request.state.customer = user["client_id"]
    return await call_next(request)


@app.exception_handler(Exception)
def exception_handler(exception: Exception) -> JSONResponse:
    """Exception Handler for all the app"""
    return process_exception(exception)


@app.get("/health_check")
async def status() -> Response:
    return Response(content="Status: OK", status_code=200)
