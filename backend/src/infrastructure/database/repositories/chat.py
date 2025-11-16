from abc import abstractmethod, ABC
from sqlalchemy import select

from backend.src.infrastructure.database.repositories.base import GenericSqlRepository
from backend.src.infrastructure.database.models.chat import ChatModel
from backend.src.core.domain.chat import ChatDTO


class ChatReposityBase(GenericSqlRepository[ChatModel, ChatDTO], ABC):
    _model = ChatModel
    _object = ChatDTO

    @abstractmethod
    async def delete_chat(self, chat_id: str) -> bool:
        raise NotImplementedError


class ChatRepository(ChatReposityBase):
    async def create_chat(self, chat_name: str) -> int:
        chat = self._model(name=chat_name)

        self._session.add(chat)
        await self._session.commit()
        return chat.id

    async def delete_chat(self, chat_id: int) -> bool:
        stmt = select(self._model).where(self._model.id == chat_id)
        result = await self._session.execute(stmt)
        chat = result.scalars().first()

        if chat is None:
            return False

        await self._session.delete(chat)
        await self._session.commit()

        return True

    async def chat_exists(self, chat_id: str) -> bool:
        stmt = select(self._model.id).where(self._model.id == chat_id)
        result = await self._session.execute(stmt)
        return result.scalars().first() is not None


    async def get_chats_list(self) -> list[tuple[int, str]]:
        stmt = select(self._model.id, self._model.name)
        result = await self._session.execute(stmt)
        return result.all()