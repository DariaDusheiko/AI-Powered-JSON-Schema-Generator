import bcrypt
from argon2 import PasswordHasher, exceptions
from abc import abstractmethod, ABC
from sqlalchemy import select, update

from backend.src.infrastructure.database.repositories.base import GenericRepository, GenericSqlRepository
from backend.src.infrastructure.database.models.schema import SchemaModel
from backend.src.core.domain.schema import SchemaDTO
from backend.src.presentation.api.exceptions import EntityNotFound


class SchemaReposityBase(GenericSqlRepository[SchemaModel, SchemaDTO], ABC):
    _model = SchemaModel
    _object = SchemaDTO

    @abstractmethod
    async def get_schema_by_id(self, id_: int, user_id: int) -> SchemaDTO:
        raise NotImplementedError
    
    @abstractmethod
    async def list_schemas(self, chat_id: int, user_id: int) -> list[SchemaDTO]:
        raise NotImplementedError

class SchemaRepository(SchemaReposityBase):
    async def get_schema_by_id(self, id_: int, user_id: int) -> SchemaDTO:
        schema = await self._get_model_by_id(id=id_)
    
        if schema.chat.user_id != user_id:
            raise EntityNotFound

        return self._convert_model_to_dto(schema)

    async def delete_by_chat_id(self, chat_id: int) -> SchemaDTO:
        stmt = select(self._model).where(self._model.chat_id == chat_id)
        result = await self._session.execute(stmt)
        schemas = result.scalars().all()

        if not schemas:
            return False

        for schema in schemas:
            await self._session.delete(schema)

        await self._session.commit()

        return True
    
    async def list_schemas(self, chat_id: int, user_id: int) -> list[SchemaDTO]:
        return [
            self._convert_model_to_dto(schema)
            for schema in (
                await self._session.execute(
                    select(self._model)
                    .where(
                        self._model.chat_id == chat_id,
                        self._model.chat.has(user_id=user_id)
                    )
                )
            ).scalars().all()
        ]

    async def set_schema(self, id_: int, schema: dict) -> None:
        stmt = (
            update(self._model)
            .where(self._model.id == id_)
            .values(schema=schema)
        )

        await self._session.execute(stmt)
        await self._session.commit()