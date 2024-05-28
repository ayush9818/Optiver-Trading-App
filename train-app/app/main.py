from fastapi import FastAPI
from app.routers import train, inference
import logging
import logging.config

# Configure logger
logging.config.fileConfig(
    "app/configs/logging/local.ini", disable_existing_loggers=False
)
logger = logging.getLogger("optiver." + __name__)

# Create FastAPI app
app = FastAPI()

# Include routers for train and inference endpoints
app.include_router(train.router)
app.include_router(inference.router)


@app.get("/healthcheck/")
def healthcheck():
    """
    Healthcheck endpoint to verify if the service is running.

    Returns:
        dict: A message indicating the service is healthy.
    """
    logger.info("Healthcheck endpoint called.")
    return {"message": "Healthy"}


if __name__ == "__main__":
    import uvicorn

    logger.info("Starting the FastAPI application using Uvicorn.")
    uvicorn.run("app.main:app", host="0.0.0.0", port=8001, reload=True)
