"""
Main FastAPI application with single-port deployment
"""
import sys
from pathlib import Path

# Add project root to Python path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from fastapi import FastAPI, Request, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import JSONResponse, FileResponse
from contextlib import asynccontextmanager
import logging
import time
from pathlib import Path

from backend.config import get_settings
from backend.core.logging_config import setup_logging, set_correlation_id
from backend.database import init_db
from backend.api import auth_router, upload_router, match_router, search_router

settings = get_settings()

# Setup logging
setup_logging(settings.LOG_LEVEL)
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Lifespan events for startup and shutdown
    """
    # Startup
    logger.info("Starting AI Job Matcher application...")
    try:
        init_db()
        logger.info("Database initialized successfully")
    except Exception as e:
        logger.error(f"Failed to initialize database: {e}")
        raise
    
    yield
    
    # Shutdown
    logger.info("Shutting down AI Job Matcher application...")


# Create FastAPI app
app = FastAPI(
    title="AI Job Matcher API",
    description="AI-powered candidate and job matching platform using NLP and semantic embeddings",
    version="1.0.0",
    lifespan=lifespan
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify exact origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.middleware("http")
async def correlation_id_middleware(request: Request, call_next):
    """
    Add correlation ID to each request
    """
    correlation_id = request.headers.get("X-Correlation-ID")
    set_correlation_id(correlation_id)
    
    response = await call_next(request)
    response.headers["X-Correlation-ID"] = correlation_id or ""
    return response


@app.middleware("http")
async def logging_middleware(request: Request, call_next):
    """
    Log all requests and responses
    """
    start_time = time.time()
    
    # Log request
    logger.info(f"Request: {request.method} {request.url.path}")
    
    try:
        response = await call_next(request)
        process_time = time.time() - start_time
        
        # Log response
        logger.info(
            f"Response: {request.method} {request.url.path} "
            f"Status: {response.status_code} Time: {process_time:.3f}s"
        )
        
        response.headers["X-Process-Time"] = str(process_time)
        return response
    
    except Exception as e:
        logger.error(f"Request failed: {request.method} {request.url.path} Error: {e}")
        raise


@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    """
    Global exception handler for unified error responses
    """
    logger.error(f"Unhandled exception: {exc}", exc_info=True)
    
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={
            "error": "Internal server error",
            "detail": str(exc) if settings.DEBUG else "An unexpected error occurred",
        }
    )


# Include API routers
app.include_router(auth_router)
app.include_router(upload_router)
app.include_router(match_router)
app.include_router(search_router)


@app.get("/api/health")
async def health_check():
    """
    Health check endpoint
    """
    return {
        "status": "healthy",
        "app": settings.APP_NAME,
        "environment": settings.APP_ENV
    }


# Serve React frontend (after build)
frontend_dist = Path(__file__).parent.parent / "frontend" / "dist"
if frontend_dist.exists():
    # Serve static files (JS, CSS, images)
    app.mount("/assets", StaticFiles(directory=str(frontend_dist / "assets")), name="assets")
    
    # Catch-all route for React Router - must be last
    @app.get("/{full_path:path}")
    async def serve_frontend(full_path: str):
        """
        Serve React app for all non-API routes
        """
        # If file exists, serve it
        file_path = frontend_dist / full_path
        if file_path.is_file():
            return FileResponse(file_path)
        
        # Otherwise serve index.html for React Router
        return FileResponse(frontend_dist / "index.html")
    
    logger.info(f"Serving frontend from {frontend_dist}")
else:
    logger.warning(f"Frontend dist directory not found: {frontend_dist}")
    
    @app.get("/")
    async def root():
        return {
            "message": "AI Job Matcher API",
            "docs": "/docs",
            "health": "/api/health"
        }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=settings.PORT,
        reload=settings.DEBUG
    )
