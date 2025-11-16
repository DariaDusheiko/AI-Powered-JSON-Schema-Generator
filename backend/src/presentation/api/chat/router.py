from fastapi import APIRouter, Depends, Request
from starlette import status

from backend.src.infrastructure.database.unit_of_work import UnitOfWork, get_unit_of_work
from backend.src.presentation.api.chat.schema import ChatsListResponse, ChatListItem
from backend.src.presentation.api.auth.utils import protect

chat_router = APIRouter(prefix="/chats", tags=["chats"])


@chat_router.get(
    path="/list",
    status_code=status.HTTP_200_OK,
    summary="Get list of all chats",
    response_model=ChatsListResponse,
)
@protect()
async def get_chats_list(
    request: Request,
    uow: UnitOfWork = Depends(get_unit_of_work)
) -> ChatsListResponse:
    chats = await uow.chat.list(user_id=request.state.user_id)
    return ChatsListResponse(
        chats=[
            ChatListItem(
                chat_id=chat.id,
                chat_name=chat.name
            )
            for chat in chats
        ]
    )


@chat_router.delete(
    path="",
    status_code=status.HTTP_200_OK,
    summary="Delete chat by id",
    response_model=ChatsListResponse,
)
@protect()
async def delete_chat(
    request: Request,
    chat_id: int,
    uow: UnitOfWork = Depends(get_unit_of_work)
) -> ChatsListResponse:
    await uow.schema.delete_by_chat_id(chat_id=chat_id)
    await uow.chat.delete_chat(chat_id=chat_id)

    chats = await uow.chat.list(user_id=request.state.user_id)
    return ChatsListResponse(
        chats=[
            ChatListItem(
                chat_id=chat.id,
                chat_name=chat.name
            )
            for chat in chats
        ]
    )

