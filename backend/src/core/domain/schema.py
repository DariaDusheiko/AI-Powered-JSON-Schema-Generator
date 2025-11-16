import datetime
from typing import Any
from backend.src.core.domain.base import BaseDTO


class SchemaDTO(BaseDTO):
    id: int
    chat_id: int
    schema: dict[str, Any] | None
    user_message: str
    bot_message: str | None
    created_at: datetime.datetime | None = None
