from backend.src.core.domain.base import BaseDTO
import datetime


class ChatDTO(BaseDTO):
    id: int | None = None
    name: str
    user_id: int
    created_at: datetime.datetime | None = None
