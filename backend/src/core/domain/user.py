from backend.src.core.domain.base import BaseDTO
import datetime


class UserDTO(BaseDTO):
    username: str
    password: str

    # created_at: datetime