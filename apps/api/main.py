"""
Homlo API - Main application entry point
Pakistan-first Airbnb-style marketplace backend
"""

import os
import time
from contextlib import asynccontextmanager
from typing import List

import uvicorn
from fastapi import FastAPI, Request, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles
from prometheus_client import Counter, Histogram
from starlette.middleware.base import BaseHTTPMiddleware

from app.core.config import settings
from app.core.database import engine
from app.core.logging import setup_logging
from app.api.v1.api import api_router
from app.core.celery import celery_app
from app.core.redis import redis_client

# Prometheus metrics
REQUEST_COUNT = Counter("http_requests_total", "Total HTTP requests", ["method", "endpoint", "status"])
REQUEST_LATENCY = Histogram("http_request_duration_seconds", "HTTP request latency")

# Setup logging
logger = setup_logging()


class MetricsMiddleware(BaseHTTPMiddleware):
    """Middleware to collect Prometheus metrics"""
    
    async def dispatch(self, request: Request, call_next):
        start_time = time.time()
        
        response = await call_next(request)
        
        # Record metrics
        duration = time.time() - start_time
        REQUEST_COUNT.labels(
            method=request.method,
            endpoint=request.url.path,
            status=response.status_code
        ).inc()
        REQUEST_LATENCY.observe(duration)
        
        return response


class LoggingMiddleware(BaseHTTPMiddleware):
    """Middleware for request logging"""
    
    async def dispatch(self, request: Request, call_next):
        start_time = time.time()
        
        # Log request
        logger.info(
            f"Request: {request.method} {request.url.path}",
            extra={
                "method": request.method,
                "path": request.url.path,
                "client_ip": request.client.host if request.client else None,
                "user_agent": request.headers.get("user-agent"),
            }
        )
        
        response = await call_next(request)
        
        # Log response
        duration = time.time() - start_time
        logger.info(
            f"Response: {response.status_code} in {duration:.3f}s",
            extra={
                "status_code": response.status_code,
                "duration": duration,
            }
        )
        
        return response


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan events"""
    # Startup
    logger.info("Starting Homlo API...")
    
    # Test database connection
    try:
        # Test Redis connection
        await redis_client.ping()
        logger.info("Redis connection established")
        
        # Test database connection
        async with engine.begin() as conn:
            await conn.execute("SELECT 1")
        logger.info("Database connection established")
        
    except Exception as e:
        logger.error(f"Failed to establish connections: {e}")
        raise
    
    logger.info("Homlo API started successfully")
    
    yield
    
    # Shutdown
    logger.info("Shutting down Homlo API...")
    
    # Close connections
    await engine.dispose()
    await redis_client.close()
    
    logger.info("Homlo API shutdown complete")


def create_application() -> FastAPI:
    """Create and configure FastAPI application"""
    
    # Create FastAPI app
    app = FastAPI(
        title=settings.APP_NAME,
        version=settings.APP_VERSION,
        description="Pakistan-first Airbnb-style marketplace API",
        docs_url="/docs" if settings.DEBUG else None,
        redoc_url="/redoc" if settings.DEBUG else None,
        openapi_url="/openapi.json" if settings.DEBUG else None,
        lifespan=lifespan,
    )
    
    # Add middleware
    app.add_middleware(LoggingMiddleware)
    app.add_middleware(MetricsMiddleware)
    
    # CORS middleware
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.CORS_ORIGINS,
        allow_credentials=settings.CORS_ALLOW_CREDENTIALS,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    
    # Trusted host middleware
    if not settings.DEBUG:
        app.add_middleware(
            TrustedHostMiddleware,
            allowed_hosts=["*"]  # Configure appropriately for production
        )
    
    # Global exception handler
    @app.exception_handler(Exception)
    async def global_exception_handler(request: Request, exc: Exception):
        logger.error(f"Unhandled exception: {exc}", exc_info=True)
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={"detail": "Internal server error"}
        )
    
    # Health check endpoint
    @app.get("/healthz")
    async def health_check():
        """Health check endpoint for load balancers"""
        return {"status": "healthy", "timestamp": time.time()}
    
    # Metrics endpoint for Prometheus
    @app.get("/metrics")
    async def metrics():
        """Prometheus metrics endpoint"""
        from prometheus_client import generate_latest
        return Response(generate_latest(), media_type="text/plain")
    
    # Ready check endpoint
    @app.get("/readyz")
    async def ready_check():
        """Ready check endpoint for Kubernetes"""
        try:
            # Test database connection
            async with engine.begin() as conn:
                await conn.execute("SELECT 1")
            
            # Test Redis connection
            await redis_client.ping()
            
            return {"status": "ready", "timestamp": time.time()}
        except Exception as e:
            logger.error(f"Ready check failed: {e}")
            return JSONResponse(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                content={"status": "not ready", "error": str(e)}
            )
    
    # Include API router
    app.include_router(api_router, prefix="/api/v1")
    
    # Mount static files
    app.mount("/static", StaticFiles(directory="uploads"), name="static")
    
    return app


# Create application instance
app = create_application()


if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=settings.DEBUG,
        log_level=settings.LOG_LEVEL.lower(),
    )
