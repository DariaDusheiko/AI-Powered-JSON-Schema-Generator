from typing import Any
from fastapi import Request, HTTPException
from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware

class AuthMiddleware(BaseHTTPMiddleware):
    @staticmethod
    async def dispatch(request: Request, call_next):
        try:
            request.state.access_token = request.headers.get('X-Auth-Token')
            user_id = request.headers.get('X-UID')
            if user_id not in (None, "", "undefined"):
                request.state.user_id = int(user_id)
            else:
                request.state.user_id = None

            response = await call_next(request)

            return response

        except HTTPException as exc:
            return JSONResponse(content={"detail": exc.detail}, status_code=exc.status_code)
        except Exception as exc:
            return JSONResponse(content={"detail": f"Error: {str(exc)}"}, status_code=500)
