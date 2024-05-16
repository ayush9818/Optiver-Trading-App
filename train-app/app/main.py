from fastapi import FastAPI
from app.routers import train, inference

app = FastAPI()

app.include_router(train.router)
app.include_router(inference.router)

@app.get("/healthcheck/")
def healthcheck():
    return {"message": "Healthy"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="0.0.0.0", port=8001, reload=True)
