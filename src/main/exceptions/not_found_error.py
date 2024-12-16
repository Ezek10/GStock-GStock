from src.main.exceptions.base_error import ApplicationError


class NotFoundError(ApplicationError):
    def __init__(self, *args: object) -> None:
        super().__init__(*args)
