from backend.src.presentation.api.base.schema import BaseRequest, BaseResponse


class LoginRequest(BaseRequest):
    username: str
    password: str


class AuthResponse(BaseResponse):
    user_id: int
    access_token: str