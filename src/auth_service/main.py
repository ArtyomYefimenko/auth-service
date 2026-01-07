import logging

from fastapi import (
    APIRouter,
    FastAPI,
    status,
)
from fastapi.responses import JSONResponse

from auth_service.api.health import router as health_router
from auth_service.api.public.v1.auth import router as auth_router
from auth_service.core.config import settings
from auth_service.core.errors import BaseApiError

logger = logging.getLogger(__name__)


def create_application() -> FastAPI:
    """
    Create an application.

    Returns:
        The application as `FastAPI`.
    """
    app = FastAPI(debug=settings.debug)

    @app.exception_handler(BaseApiError)
    async def base_api_error_handler(request, exc: BaseApiError):
        return JSONResponse(
            status_code=exc.status_code,
            content={
                'details': exc.message,
                'error_code': exc.error_code,
            },
        )

    @app.exception_handler(Exception)
    async def internal_error_handler(request, exc: Exception):
        logger.error('Unhandled exception', exc_info=True)
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={'details': 'Server error'},
        )

    v1_router = APIRouter(prefix='/api/v1')
    v1_router.include_router(auth_router)

    app.include_router(health_router)
    app.include_router(v1_router)

    return app


application = create_application()
