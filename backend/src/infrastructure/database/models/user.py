from sqlalchemy import Column, Index
from sqlalchemy.dialects.postgresql import TEXT, INTEGER
from sqlalchemy.orm import relationship
from backend.src.infrastructure.database import DeclarativeBase


class UserModel(DeclarativeBase):
    __tablename__ = "users"

    id = Column(INTEGER(), primary_key=True, autoincrement=True)
    username = Column(TEXT(), nullable=False, index=True)
    password = Column(TEXT(), nullable=False)

    chats = relationship("ChatModel", back_populates="user")
    