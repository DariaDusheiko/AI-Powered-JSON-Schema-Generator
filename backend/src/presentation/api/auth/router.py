from fastapi import APIRouter, Request, Depends, HTTPException
from starlette import status

from backend.src.presentation.api.auth.utils import protect, create_access_token
from backend.src.presentation.api.auth.schema import LoginRequest, AuthResponse
from backend.src.infrastructure.database.unit_of_work import UnitOfWork, get_unit_of_work
from backend.src.presentation.api.exceptions import InvalidCredentials
from backend.src.core.domain.user import UserDTO

auth_router = APIRouter(prefix="/auth", tags=["auth"])


@auth_router.post(
    path="/login",
    status_code=status.HTTP_200_OK,
    summary="Authenticate or register user",
    response_model=AuthResponse,
)
async def login_or_register(
        request: Request,
        auth_data: LoginRequest,
        uow: UnitOfWork = Depends(get_unit_of_work),
):
    user = await uow.user.get_by_username(auth_data.username)

    if user:
        credentials_valid = await uow.user.validate_credentials(
            username=auth_data.username,
            password=auth_data.password
        )
        if not credentials_valid:
            raise InvalidCredentials
    else:
        user = await uow.user.add(
            UserDTO(
                username=auth_data.username,
                password=auth_data.password,
            )
        )
        await uow.commit()

    token = create_access_token(
        data={"user_id": user.id, "username": user.username}
    )

    return AuthResponse(
        user_id=user.id,
        access_token=token['access_token'],
    )