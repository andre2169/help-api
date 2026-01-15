from fastapi import Request
from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware

from app.core.exceptions import (
    TicketNotFound,
    TicketInvalidStatus,
    TicketPermissionDenied,
    InvalidCredentials,
)


class ExceptionMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        try:
            return await call_next(request)

        except TicketNotFound as e:
            return JSONResponse(
                status_code=404,
                content={"detail": str(e) or "Ticket não encontrado"},
            )

        except TicketInvalidStatus as e:
            return JSONResponse(
                status_code=400,
                content={"detail": str(e) or "Status inválido para esta ação"},
            )

        except TicketPermissionDenied as e:
            return JSONResponse(
                status_code=403,
                content={"detail": str(e) or "Permissão negada"},
            )

        except InvalidCredentials as e:
            return JSONResponse(
                status_code=401,
                content={"detail": str(e) or "Credenciais inválidas"},
            )

        except Exception:
            # fallback de segurança
            return JSONResponse(
                status_code=500,
                content={"detail": "Erro interno do servidor"},
            )
