from fastapi.responses import JSONResponse

from src.main.exceptions.already_exist_error import AlreadyExistError
from src.main.exceptions.already_sold_error import ItemNotAvailableError
from src.main.exceptions.base_error import ApplicationError
from src.main.exceptions.not_found_error import NotFoundError
from src.main.exceptions.unauthorized_error import UnauthorizedError


def process_exception(exception: Exception) -> JSONResponse:
    """Exception to JSONResponse handler"""
    if isinstance(exception, UnauthorizedError):
        response = JSONResponse(status_code=401, content="Unauthorized")

    elif isinstance(exception, AlreadyExistError):
        response = JSONResponse(status_code=400, content="Object Already Exist")

    elif isinstance(exception, ItemNotAvailableError):
        response = JSONResponse(status_code=400, content="Item Not Available")

    elif isinstance(exception, NotFoundError):
        response = JSONResponse(status_code=404, content="NotFound")

    elif isinstance(exception, ApplicationError):
        response = JSONResponse(status_code=500, content="Application Exception")

    else:
        response = JSONResponse(status_code=500, content="Internal Server Error")

    response.headers["Access-Control-Allow-Origin"] = "*"
    response.headers["Access-Control-Allow-Methods"] = "DELETE, GET, HEAD, OPTIONS, PATCH, POST, PUT"
    response.headers["Access-Control-Allow-Headers"] = "Authorization, Content-Type, use_cache, cache-control"

    return response
