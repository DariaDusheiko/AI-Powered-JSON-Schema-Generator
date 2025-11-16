from pydantic import BaseModel


class BaseDTO(BaseModel):
    id: int | None = None

    class Config:
        from_attributes = True