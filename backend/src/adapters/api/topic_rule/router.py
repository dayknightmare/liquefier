# from src.adapters.api.topic.controllers.detail import TopicDetailController
from src.adapters.api.topic_rule.controllers.list import TopicRuleListController
from src.adapters.api.topic_rule.controllers.add import TopicRuleAddController
from fastapi import APIRouter, Depends, status, Request, Response
from src.adapters.spi.repository_factory import RepositoryFactory
from src.dto.response import ErrorResponseDTO, SucessResponseDTO
from src.dto.topic_rule.list_dto import TopicRuleListDTO
from src.domain.topic_rule_entity import TopicRuleEntity
from src.dto.topic_rule.add_dto import TopicRuleAddDTO
from src.middleware.params import parse_param
from fastapi_injector import Injected


topic_rule_router = APIRouter(
    prefix="/topic_rule",
    dependencies=[
        # Depends(jwt_auth),
    ],
)


@topic_rule_router.get(
    "/list",
    responses={
        status.HTTP_200_OK: {
            "description": "OK",
            "model": SucessResponseDTO[list[TopicRuleEntity]],
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
    filters: TopicRuleListDTO = Depends(parse_param(TopicRuleListDTO)),
):
    return await TopicRuleListController(
        request,
        response,
        repository.get_repositories("topic_rule_repository"),
    ).handle(
        filters,
        page,
    )


# @topic_rule_router.get(
#     "/detail/{id}",
#     responses={
#         status.HTTP_200_OK: {
#             "description": "OK",
#             "model": SucessResponseDTO[TopicRuleEntity | None],
#         },
#         status.HTTP_400_BAD_REQUEST: {
#             "description": "Wrong request body",
#             "model": ErrorResponseDTO,
#         },
#     },
# )
# async def detail_topic(
#     id: str,
#     request: Request,
#     response: Response,
#     repository: RepositoryFactory = Injected(RepositoryFactory),
# ):
#     return await TopicDetailController(
#         request,
#         response,
#         repository.get_repositories("topic_repository"),
#     ).handle(id)


@topic_rule_router.post(
    "/add",
    responses={
        status.HTTP_201_CREATED: {
            "description": "Created",
            "model": SucessResponseDTO[TopicRuleEntity],
        },
        status.HTTP_400_BAD_REQUEST: {
            "description": "Wrong request body",
            "model": ErrorResponseDTO,
        },
    },
    status_code=201,
)
async def add_topic_rule(
    data: TopicRuleAddDTO,
    request: Request,
    response: Response,
    repository: RepositoryFactory = Injected(RepositoryFactory),
):
    response.status_code = 201
    return await TopicRuleAddController(
        request,
        response,
        repository.get_repositories("topic_rule_repository"),
    ).handle(
        data,
    )
