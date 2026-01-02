"""API package."""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import sys
from pathlib import Path

# Add src to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from config import config
from services.logging.logger import logger_instance as logger
from api.routes.nl_queries import router as nl_queries_router


def create_app() -> FastAPI:
    """Create and configure FastAPI application."""
    app = FastAPI(title="Natural Language Inventory Dashboard API")
    
    # CORS middleware
    app.add_middleware(
        CORSMiddleware,
        allow_origins=[config.CORS_ORIGIN],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    
    # Request logging middleware
    @app.middleware("http")
    async def log_requests(request, call_next):
        logger.info(f"{request.method} {request.url.path}", {
            'ip': request.client.host if request.client else None,
            'userAgent': request.headers.get('user-agent'),
        })
        response = await call_next(request)
        return response
    
    # Routes
    app.include_router(nl_queries_router, prefix="/api", tags=["nl-queries"])
    
    return app
