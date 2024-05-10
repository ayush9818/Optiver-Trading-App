from fastapi import FastAPI, Depends, HTTPException, Query, status
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from sqlalchemy.orm import Session
from database import SessionLocal
from models import (
    IngestRequest, 
    DateMappingQueryParams, 
    DateMappingRequest, 
    StockDataRequest, 
    StockDataQueryParams,
    PageRequest,
    PageDateRequest,
    ModelCreate,
    ModelDisplay,
    PageModelRequest, 
    ModelInferenceCreate,
    PageModelInference,
    ModelInferenceRead
)
from crud import get_or_create_date
from schema import StockData, DateMapping, Model
from utils import apply_filters, clean_nan_values
from datetime import date
import math
import json
import uvicorn
from typing import List, Optional, Any

app = FastAPI()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/healtcheck/")
def hello():
    return {"message" : "Healthy"}

@app.post("/ingest/")
async def ingest_data(request: IngestRequest, db: Session = Depends(get_db)):
    try:
        for item in request.data:
            date_mapping = get_or_create_date(db, item.date_id)
            db.add(StockData(**item.dict(), date_mapping=date_mapping))
        if request.commit:
            db.commit()
        return {"message": "Data ingested successfully."}
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/date_mappings/", response_model=PageDateRequest)
def get_date_mappings(query_params: DateMappingQueryParams = Depends(),
                      db: Session = Depends(get_db),
                      page: int = Query(1, description="Page number"),
                      page_size: int = Query(10, description="Number of results per page")
                     ):
    query_params = query_params.dict(exclude_none=True)
    query = db.query(DateMapping)
    query = apply_filters(query, DateMapping, query_params)
    total_results = query.count()

    # Calculate offset and limit based on page and page_size
    offset = (page - 1) * page_size
    query = query.offset(offset).limit(page_size)

    results = query.all()

    if not results:
        raise HTTPException(status_code=404, detail="No date mappings found matching the criteria.")

    total_pages = (total_results + page_size - 1) // page_size

    return {
        "total_results": total_results,
        "total_pages": total_pages,
        "page": page,
        "page_size": page_size,
        "data": results
    }

@app.get("/get_stock_data/", response_model=PageRequest)
def get_stock_data(
    query_params: StockDataQueryParams = Depends(),
    db: Session = Depends(get_db),
    page: int = Query(1, description="Page number"),
    page_size: int = Query(10, description="Number of results per page")
):
    query = db.query(StockData)
    if query_params.start_date_id and query_params.end_date_id:
        query = query.filter(StockData.date_id.between(query_params.start_date_id, query_params.end_date_id))
    elif query_params.date_id:
        query = query.filter(StockData.date_id == query_params.date_id)
    else:
        raise HTTPException(status_code=400, detail="Please provide either a valid date range or valid date id")
    
    total_results = query.count()

    # Calculate offset and limit based on page and page_size
    offset = (page - 1) * page_size
    query = query.offset(offset).limit(page_size)

    results = query.all()

    if not results:
        raise HTTPException(status_code=404, detail="No stock data found matching the criteria.")
    cleaned_results = [clean_nan_values(result.__dict__) for result in results]
    total_pages = (total_results + page_size - 1) // page_size

    return {
        "total_results": total_results,
        "total_pages": total_pages,
        "page": page,
        "page_size": page_size,
        "data": cleaned_results
    }

@app.post("/models/")
async def create_model(model: ModelCreate, db: Session = Depends(get_db)):
    existing_model = db.query(Model).filter(Model.model_name == model.model_name).first()
    if existing_model:
        raise HTTPException(status_code=400, detail="Model already exists")
    new_model = Model(model_name=model.model_name, model_artifact_path=model.model_artifact_path)
    db.add(new_model)
    try:
        db.commit()
    except exc.IntegrityError:
        db.rollback()
        raise HTTPException(status_code=400, detail="Model with this name already exists")
    db.refresh(new_model)
    return {"message": "Model Created successfully."}

@app.get("/models/", response_model=PageModelRequest)
def read_models(db: Session = Depends(get_db), page: int = Query(1, description="Page number"), page_size: int = Query(10, description="Number of results per page")):
    query = db.query(Model)
    total_results = query.count()
    # Calculate offset and limit based on page and page_size
    offset = (page - 1) * page_size
    query = query.offset(offset).limit(page_size)
    results = query.all()
    if not results:
        raise HTTPException(status_code=404, detail="No Models Found.")

    total_pages = (total_results + page_size - 1) // page_size
    return {
        "total_results": total_results,
        "total_pages": total_pages,
        "page": page,
        "page_size": page_size,
        "data": results
    }


@app.get("/models/{model_id}", response_model=PageModelRequest)
def read_model(model_id: int, 
              db: Session = Depends(get_db), 
              page: int = Query(1, description="Page number"), 
              page_size: int = Query(10, description="Number of results per page")):
    query = db.query(Model).filter(Model.model_id == model_id)
    total_results = query.count()
    # Calculate offset and limit based on page and page_size
    offset = (page - 1) * page_size
    query = query.offset(offset).limit(page_size)
    results = query.all()
    if not results:
        raise HTTPException(status_code=404, detail="No Models Found.")

    total_pages = (total_results + page_size - 1) // page_size
    return {
        "total_results": total_results,
        "total_pages": total_pages,
        "page": page,
        "page_size": page_size,
        "data": results
    }

@app.post("/model-inferences/", response_model=ModelInferenceRead, status_code=status.HTTP_201_CREATED)
def create_model_inference(model_inference: ModelInferenceCreate, db: Session = Depends(get_db)):
    try:
        db_model_inference = ModelInference(**model_inference.dict())
        db.add(db_model_inference)
        db.commit()
        db.refresh(db_model_inference)
        return db_model_inference
    except IntegrityError as e:
        db.rollback()
        raise HTTPException(status_code=400, detail="Could not create model inference. Possible duplicate or missing required foreign key.")
    except SQLAlchemyError as e:
        db.rollback()
        raise HTTPException(status_code=500, detail="Internal server error.")
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/model-inferences/", response_model=PageModelInference)
def read_model_inferences(model_id: int, 
                         date_id: int, 
                         db: Session = Depends(get_db),
                         page: int = Query(1, description="Page number"), 
                         page_size: int = Query(10, description="Number of results per page")
                         ):
    query = db.query(ModelInference).filter(
        ModelInference.model_id == model_id, 
        ModelInference.date_id == date_id
    )
    total_results = query.count()
    # Calculate offset and limit based on page and page_size
    offset = (page - 1) * page_size
    query = query.offset(offset).limit(page_size)
    results = query.all()
    if not results:
        raise HTTPException(status_code=404, detail="Model inference not found.")

    total_pages = (total_results + page_size - 1) // page_size
    return {
        "total_results": total_results,
        "total_pages": total_pages,
        "page": page,
        "page_size": page_size,
        "data": results
    }


if __name__ == "__main__":
    uvicorn.run("app:app", host="0.0.0.0", port=8000, reload=True)
