from sqlalchemy import Column, DateTime, ForeignKey
from sqlalchemy.dialects.postgresql import TEXT, INTEGER
from sqlalchemy.orm import relationship
from datetime import datetime
from backend.src.infrastructure.database import DeclarativeBase


class ChatModel(DeclarativeBase):
    __tablename__ = "chats"

    id = Column(INTEGER(), primary_key=True, autoincrement=True)
    name = Column(TEXT(), default="")
    created_at = Column(DateTime(), default=datetime.now, nullable=False)
    user_id = Column(INTEGER(), ForeignKey("users.id"), index=True)
    
    user = relationship("UserModel", back_populates="chats")
    schemas = relationship("SchemaModel", back_populates="chat")