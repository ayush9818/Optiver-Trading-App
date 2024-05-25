from fastapi import FastAPI
from app.routers import date_mappings, stock_data, models, model_inferences

import logging
import logging.config

# Configure logger
logging.config.fileConfig('app/configs/logging/local.ini', disable_existing_loggers=False)
logger = logging.getLogger('optiver.' + __name__)

app = FastAPI()

# Include routers from different modules
app.include_router(date_mappings.router)
app.include_router(stock_data.router)
app.include_router(models.router)
app.include_router(model_inferences.router)

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
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)
