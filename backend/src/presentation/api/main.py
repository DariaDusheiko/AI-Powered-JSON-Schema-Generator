import asyncio
from fastapi import FastAPI
from fastapi_pagination import add_pagination
from fastapi.middleware.cors import CORSMiddleware

from backend.src.config import Config, settings
from backend.src.presentation.api import list_of_routes
from backend.src.presentation.api.middleware import AuthMiddleware


def bind_routes(application: FastAPI, setting: Config) -> None:
    for route in list_of_routes:
        application.include_router(route, prefix=setting.app.path_prefix)


def get_app() -> FastAPI:
    description = "API JSON-schemas"

    tags_metadata = [
        {
            "name": "JSON-schemas",
            "description": "Creating JSON-schemas with MWS_Gpt",
        },
    ]

    application = FastAPI(
        title="JSON-schemas",
        description=description,
        docs_url=f"{settings.app.path_prefix}/swagger",
        openapi_url=f"{settings.app.path_prefix}/openapi",
        version="0.1.0",
        openapi_tags=tags_metadata,
    )
    bind_routes(application, settings)
    add_pagination(application)
    application.state.settings = settings
    application.add_middleware(AuthMiddleware)
    application.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    return application


app = get_app()


# if __name__ == "__main__":
#     import uvicorn
#     uvicorn.run(
#         "backend.src.presentation.api.main:app",
#         host=settings.app.host,
#         port=settings.app.port,
#         reload=settings.app.reload
#     )