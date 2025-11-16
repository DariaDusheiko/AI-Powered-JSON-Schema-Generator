from pydantic import BaseModel
from typing import List, Tuple

class ChatListItem(BaseModel):
    chat_id: int
    chat_name: str

class ChatsListResponse(BaseModel):
    chats: List[ChatListItem]