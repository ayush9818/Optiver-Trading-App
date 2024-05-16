from fastapi import FastAPI
from app.routers import ingest, date_mappings, stock_data, models, model_inferences

app = FastAPI()

app.include_router(ingest.router)
app.include_router(date_mappings.router)
app.include_router(stock_data.router)
app.include_router(models.router)
app.include_router(model_inferences.router)

@app.get("/healthcheck/")
def healthcheck():
    return {"message": "Healthy"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)
