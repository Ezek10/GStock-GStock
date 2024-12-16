from src.main.exceptions.base_error import ApplicationError


class ItemNotAvailableError(ApplicationError):
    def __init__(self, *args: object) -> None:
        super().__init__(*args)
