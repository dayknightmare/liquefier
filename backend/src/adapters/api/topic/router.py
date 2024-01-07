from src.adapters.api.topic.controllers.delete import TopicDeleteController
from src.adapters.api.topic.controllers.detail import TopicDetailController
from src.adapters.api.topic.controllers.edit import TopicEditController
from src.adapters.api.topic.controllers.list import TopicListController
from src.adapters.api.topic.controllers.add import TopicAddController
from fastapi import APIRouter, Depends, status, Request, Response
from src.adapters.spi.repository_factory import RepositoryFactory
from src.dto.response import ErrorResponseDTO, SucessResponseDTO
from src.adapters.spi.stream.consumer import Stream
from src.domain.topic_entity import TopicEntity
from src.dto.topic.edit_dto import TopicEditDTO
from src.dto.topic.list_dto import TopicListDTO
from src.middleware.params import parse_param
from src.dto.topic.add_dto import TopicAddDTO
from fastapi_injector import Injected


topic_router = APIRouter(
    prefix="/topic",
    dependencies=[
        # Depends(jwt_auth),
    ],
)


@topic_router.get(
    "/list",
    responses={
        status.HTTP_200_OK: {
            "description": "OK",
            "model": SucessResponseDTO[list[TopicEntity]],
        },
        status.HTTP_400_BAD_REQUEST: {
            "description": "Wrong request body",
            "model": ErrorResponseDTO,
        },
    },
)
async def list_topic(
    request: Request,
    response: Response,
    repository: RepositoryFactory = Injected(RepositoryFactory),
    page: int | None = 0,
    filters: TopicListDTO = Depends(parse_param(TopicListDTO)),
):
    return await TopicListController(
        request,
        response,
        repository.get_repositories("topic_repository"),
    ).handle(
        filters,
        page,
    )


@topic_router.get(
    "/detail/{id}",
    responses={
        status.HTTP_200_OK: {
            "description": "OK",
            "model": SucessResponseDTO[TopicEntity | None],
        },
        status.HTTP_400_BAD_REQUEST: {
            "description": "Wrong request body",
            "model": ErrorResponseDTO,
        },
    },
)
async def detail_topic(
    id: str,
    request: Request,
    response: Response,
    repository: RepositoryFactory = Injected(RepositoryFactory),
):
    return await TopicDetailController(
        request,
        response,
        repository.get_repositories("topic_repository"),
    ).handle(id)


@topic_router.post(
    "/add",
    responses={
        status.HTTP_201_CREATED: {
            "description": "Created",
            "model": SucessResponseDTO[TopicEntity],
        },
        status.HTTP_400_BAD_REQUEST: {
            "description": "Wrong request body",
            "model": ErrorResponseDTO,
        },
    },
    status_code=201,
)
async def add_topic(
    data: TopicAddDTO,
    request: Request,
    response: Response,
    repository: RepositoryFactory = Injected(RepositoryFactory),
    stream: Stream = Injected(Stream),
):
    response.status_code = 201
    return await TopicAddController(
        request,
        response,
        repository.get_repositories("topic_repository"),
    ).handle(
        data,
        stream,
    )


@topic_router.patch(
    "/edit/{id}",
    responses={
        status.HTTP_200_OK: {
            "description": "Edited successfully",
            "model": SucessResponseDTO[TopicEntity],
        },
        status.HTTP_400_BAD_REQUEST: {
            "description": "Wrong request body",
            "model": ErrorResponseDTO,
        },
    },
)
async def edit_topic(
    data: TopicEditDTO,
    id: str,
    request: Request,
    response: Response,
    repository: RepositoryFactory = Injected(RepositoryFactory),
):
    return await TopicEditController(
        request,
        response,
        repository.get_repositories("topic_repository"),
    ).handle(
        id,
        data,
    )


@topic_router.delete(
    "/delete/{id}",
    responses={
        status.HTTP_200_OK: {
            "description": "Deleted successfully",
            "model": SucessResponseDTO[str],
        },
        status.HTTP_400_BAD_REQUEST: {
            "description": "Wrong request body",
            "model": ErrorResponseDTO,
        },
    },
)
async def delete_topic(
    id: str,
    request: Request,
    response: Response,
    repository: RepositoryFactory = Injected(RepositoryFactory),
):
    return await TopicDeleteController(
        request,
        response,
        repository.get_repositories("topic_repository"),
    ).handle(
        id,
    )
