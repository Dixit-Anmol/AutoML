"""
FastAPI Backend for AutoML Application
Main API Server
"""
from fastapi import FastAPI, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import os
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Import routers
from app.api.routes import upload, cleaning, training

# Create necessary directories
UPLOAD_DIR = Path(os.getenv("UPLOAD_DIR", "./data/uploads"))
MODELS_DIR = Path(os.getenv("MODELS_DIR", "./models"))
CLEANED_DATA_DIR = Path(os.getenv("CLEANED_DATA_DIR", "./data/cleaned"))

UPLOAD_DIR.mkdir(parents=True, exist_ok=True)
MODELS_DIR.mkdir(parents=True, exist_ok=True)
CLEANED_DATA_DIR.mkdir(parents=True, exist_ok=True)

# Create FastAPI app
app = FastAPI(
    title="AutoML API",
    description="Machine Learning API for Data Cleaning and Model Training",
    version="1.0.0",
)

# Configure CORS
origins = os.getenv("CORS_ORIGINS", "http://localhost:1321,http://localhost:5173").split(",")

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(upload.router, prefix="/api/upload", tags=["Upload"])
app.include_router(cleaning.router, prefix="/api/cleaning", tags=["Data Cleaning"])
app.include_router(training.router, prefix="/api/training", tags=["Model Training"])


@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "message": "AutoML API",
        "version": "1.0.0",
        "docs": "/docs"
    }


@app.get("/api/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "message": "API is running"
    }


# Global exception handler
@app.exception_handler(Exception)
async def global_exception_handler(request, exc):
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={"detail": str(exc), "error": "Internal server error"}
    )


if __name__ == "__main__":
    import uvicorn
    
    host = os.getenv("API_HOST", "0.0.0.0")
    port = int(os.getenv("API_PORT", 8000))
    reload = os.getenv("API_RELOAD", "True").lower() == "true"
    
    uvicorn.run("api_server:app", host=host, port=port, reload=reload)
