from src.application.repositories.repository_interface import RepositoryInterface
from fastapi import status, Request, Response
from src.utils.pretty_print import log_print
from traceback import format_exc
from typing import Callable


class ControllerInterface:
    def __init__(
        self,
        request: Request,
        response: Response,
        repository: RepositoryInterface,
    ):
        self.repository = repository
        self.request = request
        self.response = response

    async def handle(self):
        raise NotImplementedError("Handle not implemented")

    @staticmethod
    def handle_exception(func: Callable):
        async def wrapper(self, *args, **kwargs):
            try:
                return await func(self, *args, **kwargs)

            except Exception as e:
                self.response.status_code = status.HTTP_400_BAD_REQUEST
                log_print(format_exc())

                return {
                    "error": str(e),
                }

        wrapper.__name__ = func.__name__
        wrapper.__doc__ = func.__doc__

        return wrapper
