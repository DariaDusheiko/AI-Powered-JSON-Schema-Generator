from backend.src.presentation.api.auth.router import auth_router
from backend.src.presentation.api.chat.router import chat_router
from backend.src.presentation.api.schema.router import schema_router

list_of_routes = [
    auth_router,
    chat_router,
    schema_router
]