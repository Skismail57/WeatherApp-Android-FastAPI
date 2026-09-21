import logging

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware.base import BaseHTTPMiddleware

from app.api.routes import health, weather
from app.core.config import settings
from app.db.init_db import init_db

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)

logger = logging.getLogger(__name__)


class SecurityHeadersMiddleware(BaseHTTPMiddleware):
    """Add security headers to all responses."""

    async def dispatch(self, request, call_next):
        response = await call_next(request)
        response.headers["X-Content-Type-Options"] = "nosniff"
        response.headers["X-Frame-Options"] = "DENY"
        response.headers["Referrer-Policy"] = "no-referrer"
        response.headers["X-XSS-Protection"] = "1; mode=block"
        return response


app = FastAPI(title=settings.app_name, version=settings.app_version, debug=settings.debug)

app.add_middleware(SecurityHeadersMiddleware)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=False,
    allow_methods=["GET", "OPTIONS"],
    allow_headers=["*"],
)

app.include_router(health.router, prefix="/api/v1", tags=["health"])
app.include_router(weather.router, prefix="/api/v1/weather", tags=["weather"])


@app.on_event("startup")
async def startup_event():
    logger.info("Starting Weather Platform API")
    init_db()
    logger.info("Weather Platform API startup complete")


@app.get("/", response_model=dict, summary="Root endpoint")
async def root():
    """Root endpoint returning API status."""
    return {"message": "Weather Platform API is running"}
