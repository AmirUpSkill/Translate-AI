from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .api.v1.router import v1_router 
from .core.config import settings 

# Create FastAPI app
app = FastAPI(
    title=settings.app_name,
    version=settings.app_version,
    description="Translate AI Backend: STT + Translation API"
)

# Add CORS middleware (for frontend integration)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include API routers
app.include_router(v1_router)

# Health check endpoint
@app.get("/health")
async def health_check():
    return {"status": "healthy", "app": settings.app_name}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)