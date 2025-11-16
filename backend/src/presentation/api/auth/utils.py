import jwt
import datetime
from fastapi import Request
from functools import wraps

from backend.src.config import settings
from backend.src.presentation.api.exceptions import (
    TokenExpired,
    InvalidToken,
    UserIdRequired,
)


def decode_access_token(token: str):
    try:
        payload = jwt.decode(
            token,
            settings.app.secret_key,
            algorithms=[settings.app.algorithm]
        )
        return payload
    except jwt.ExpiredSignatureError:
        raise TokenExpired
    except jwt.InvalidTokenError:
        raise InvalidToken


def create_access_token(data: dict, expires_delta: datetime.timedelta | None = None):
    to_encode = data.copy()
    delta = expires_delta or datetime.timedelta(minutes=settings.app.access_token_expire_minutes)
    expire = datetime.datetime.now(datetime.timezone.utc) + delta
    to_encode.update({"exp": expire})

    encoded_jwt = jwt.encode(
        to_encode,
        settings.app.secret_key,
        algorithm=settings.app.algorithm
    )

    return {"access_token": encoded_jwt, "token_type": "bearer"}



def protect(uid_required: bool = True):
    def decorator(func):
        @wraps(func)
        async def wrapper(request: Request, *args, **kwargs):
            payload = decode_access_token(token=getattr(request.state, 'access_token', None))
            request.state.user_id = payload["user_id"]
            return await func(request, *args, **kwargs)

        return wrapper

    return decorator

