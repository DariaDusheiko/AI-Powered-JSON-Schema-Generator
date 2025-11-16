from fastapi import APIRouter, Request, Depends, HTTPException
from starlette import status

from backend.src.presentation.api.auth.utils import protect, create_access_token
from backend.src.infrastructure.database.unit_of_work import UnitOfWork, get_unit_of_work
from backend.src.presentation.api.schema.schema import (
    SchemaPostResponse,
    SchemaPostRequest,
    SchemaPatchResponse,
    SchemaPatchRequest,
    SchemaDetailsRequest,
    SchemaDetailsResponse,
    SchemaListRequest,
    SchemaListItem,
    SchemaListResponse,
    SchemaEditRequest,
)
from backend.src.presentation.api.context import context
from backend.src.core.domain.schema import SchemaDTO
from backend.src.core.domain.chat import ChatDTO


schema_router = APIRouter(prefix="/schemas", tags=["schema"])


@schema_router.post(
    path="",
    status_code=status.HTTP_201_CREATED,
    summary="Generate schema in new chat",
    response_model=SchemaPostResponse,
)
@protect()
async def add_schema(
    request: Request,
    schema_data: SchemaPostRequest,
    uow: UnitOfWork = Depends(get_unit_of_work),
) -> SchemaPostResponse:
    schema, bot_message = await context.mws_gpt.generate_schema(message=schema_data.message)
    chat_name = await context.mws_gpt.generate_chat_name(message=schema_data.message)
    
    chat = await uow.chat.add(
        ChatDTO(
            user_id=request.state.user_id,
            name=chat_name
        )
    )
    created_schema = await uow.schema.add(
        object=SchemaDTO(
            chat_id=chat.id,
            schema=schema,
            user_message=schema_data.message,
            bot_message=bot_message
        )
    )
    
    return SchemaPostResponse(
        schema=schema,
        schema_id=created_schema.id,
        chat_name=chat_name,
        bot_message=bot_message
    )


@schema_router.patch(
    path="",
    status_code=status.HTTP_200_OK,
    summary="Update schema",
    response_model=SchemaPatchResponse,
)
@protect()
async def update_schema(
    request: Request,
    schema_data: SchemaPatchRequest,
    uow: UnitOfWork = Depends(get_unit_of_work),
) -> SchemaPatchResponse:
    existing_schema = await uow.schema.get_schema_by_id(
        id_=schema_data.schema_id,
        user_id=request.state.user_id,
    )
    
    schema, bot_message = await context.mws_gpt.update_schema(
        message=schema_data.message,
        schema=existing_schema
    )
    
    await uow.schema.add(
        object=SchemaDTO(
            chat_id=existing_schema.chat_id,
            schema=schema,
            user_message=schema_data.message,
            bot_message=bot_message
        )
    )
    
    return SchemaPatchResponse(
        schema=schema,
        bot_message=bot_message
    )


@schema_router.get(
    path="",
    status_code=status.HTTP_200_OK,
    summary="Get schema detail information",
    response_model=SchemaDetailsResponse,
)
@protect()
async def get_detail_schema(
    request: Request,
    schema_data: SchemaPatchRequest,
    uow: UnitOfWork = Depends(get_unit_of_work),
) -> SchemaDetailsResponse:
    
    schema = await uow.schema.get_schema_by_id(
        id_=schema_data.schema_id,
        user_id=request.state.user_id,
    )
    
    return SchemaDetailsResponse(
        chat_id=schema.chat_id,
        user_message=schema.user_message,
        bot_message=schema.bot_message,
        schema=schema.schema,
    )


@schema_router.get(
    path="/list",
    status_code=status.HTTP_200_OK,
    summary="Get schemas list",
    response_model=SchemaListResponse,
)
@protect()
async def get_detail_schema(
    request: Request,
    schema_data: SchemaListRequest,
    uow: UnitOfWork = Depends(get_unit_of_work),
) -> SchemaListResponse:
    schemas = await uow.schema.list_schemas(
        chat_id=schema_data.chat_id,
        user_id=request.state.user_id,
    )
    return SchemaListResponse(
        items=[
            SchemaListItem(
                user_message=schema.user_message,
                bot_message=schema.bot_message,
                schema_id=schema.id,
            )
            for schema in schemas
        ]
    )


@schema_router.post(
    path="/edit",
    status_code=status.HTTP_200_OK,
    summary="Edit schema without AI",
    response_model=None,
)
@protect()
async def edit_schema(
        request: Request,
        schema_data: SchemaEditRequest,
        uow: UnitOfWork = Depends(get_unit_of_work),
) -> None:
    await uow.schema.set_schema(
        id_=schema_data.schema_id,
        schema=schema_data.schema,
    )
