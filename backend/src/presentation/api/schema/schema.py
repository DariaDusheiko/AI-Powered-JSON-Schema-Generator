from typing import Any
from pydantic import BaseModel
from pydantic import Json
from datetime import datetime
from backend.src.presentation.api.base.schema import BaseRequest, BaseResponse


class SchemaPostRequest(BaseRequest):
    message: str

class SchemaPostResponse(BaseResponse):
    schema: dict[str, Any]
    schema_id: int
    chat_name: str
    bot_message: str


class SchemaPatchRequest(BaseRequest):
    schema_id: int
    message: str

class SchemaPatchResponse(BaseResponse):
    schema: dict[str, Any]
    bot_message: str

class SchemaListRequest(BaseRequest):
    chat_id: int

class SchemaListItem(BaseModel):
    schema_id: int
    user_message: str
    bot_message: str | None = None

class SchemaListResponse(BaseResponse):
    items: list[SchemaListItem]


class SchemaDetailsRequest(BaseRequest):
    schema_id: int


class SchemaDetailsResponse(BaseResponse):
    chat_id: int
    user_message: str
    bot_message: str | None = None
    schema: dict[str, Any]


class SchemaEditRequest(BaseRequest):
    schema_id: int
    schema: dict[str, Any]
