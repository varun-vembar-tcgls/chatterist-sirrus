from fastapi import FastAPI
import uvicorn
import logging
from app.routers import leads, ai

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
)

# Create the FastAPI application
app = FastAPI(
    title="Leads API Service",
    description="API for retrieving and analyzing leads data",
    version="1.0.0"
)

# Include routers
app.include_router(leads.router)
app.include_router(ai.router)


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)