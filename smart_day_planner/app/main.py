from fastapi import FastAPI, HTTPException, BackgroundTasks
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
import uvicorn
import asyncio
from app.api.routes import router
from app.core.logger import setup_logger
from app.db.mongodb import db
from app.tasks.scheduler import check_weather_periodically
from contextlib import asynccontextmanager

background_task = None

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Lifespan events for FastAPI"""
    global background_task
    
    logger = setup_logger()
    logger.info("Starting Smart Day Planner application...")
    
    db.connect()
    
    background_task = asyncio.create_task(check_weather_periodically())
    logger.info("Background weather checker started (every 30 minutes)")
    
    yield
    
    if background_task:
        background_task.cancel()
        try:
            await background_task
        except asyncio.CancelledError:
            pass
    
    db.disconnect()
    logger.info("Application shutting down...")

app = FastAPI(title="Smart Day Planner API", lifespan=lifespan)

app.include_router(router, prefix="/api")

app.mount("/static", StaticFiles(directory="app/frontend/static"), name="static")

@app.get("/")
async def root():
    """Serve the main HTML page"""
    return FileResponse("app/frontend/templates/index.html")

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "message": "Smart Day Planner is running"}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)