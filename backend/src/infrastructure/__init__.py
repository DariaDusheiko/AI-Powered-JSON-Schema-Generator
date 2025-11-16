from fastapi import APIRouter, Request, Depends
from starlette import status

from backend.src.presentation.api.auth.utils import protect, create_access_token
from backend.src.presentation.api.auth.schema import LoginRequest, AuthResponse
from backend.src.infrastructure.database.unit_of_work import UnitOfWork, get_unit_of_work
from backend.src.presentation.api.exceptions import InvalidCredentials


auth_router = APIRouter(prefix="/auth", tags=["token"])


@auth_router.post(
    path="/login",
    status_code=status.HTTP_201_CREATED,
    summary="Generate Access Token",
    response_model=AuthResponse,
)
async def generate_access_token(
    request: Request,
    token_data: LoginRequest,
    uow: UnitOfWork = Depends(get_unit_of_work),
):
    credentials_valid = await uow.user.validate_credentials(username=token_data.username, password=token_data.password)
    if not credentials_valid:
        raise InvalidCredentials
    return create_access_token(
        data={"username": token_data.username, "password": token_data.password},
    )