from datetime import datetime
from sqlalchemy import Column, DateTime, ForeignKey, JSON, Index
from sqlalchemy.dialects.postgresql import TEXT, INTEGER, BIGINT
from sqlalchemy.orm import relationship
from backend.src.infrastructure.database import DeclarativeBase


class SchemaModel(DeclarativeBase):
    __tablename__ = "schemas"

    id = Column(INTEGER(), primary_key=True, autoincrement=True)
    chat_id = Column(INTEGER(), ForeignKey("chats.id"), nullable=False, index=True)
    schema = Column(JSON, default={})
    user_message = Column(TEXT(), nullable=False)
    bot_message = Column(TEXT(), nullable=True)
    created_at = Column(DateTime(), default=datetime.now, nullable=False)

    chat = relationship("ChatModel", back_populates="schemas", lazy="joined")