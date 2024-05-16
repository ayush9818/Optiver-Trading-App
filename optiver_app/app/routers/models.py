from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from app.database import get_db
from app.models import ModelCreate, PageModelRequest
from app.schema import Model
from typing import Optional

router = APIRouter()

@router.post("/models/")
async def create_model(model: ModelCreate, db: Session = Depends(get_db)):
    existing_model = db.query(Model).filter(Model.model_name == model.model_name).first()
    if existing_model:
        raise HTTPException(status_code=400, detail="Model already exists")
    new_model = Model(model_name=model.model_name, model_artifact_path=model.model_artifact_path)
    db.add(new_model)
    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=400, detail="Model with this name already exists")
    db.refresh(new_model)
    return {"message": "Model Created successfully."}

@router.get("/models/", response_model=PageModelRequest)
def read_model(
    model_id: Optional[int] = Query(None, description="Model ID"),
    model_name: Optional[str] = Query(None, description="Model Name"),
    page: int = Query(1, description="Page number"),
    page_size: int = Query(10, description="Number of results per page"),
    db: Session = Depends(get_db)
):
    query = db.query(Model)

    if model_id is not None:
        query = query.filter(Model.model_id == model_id)
    elif model_name is not None:
        query = query.filter(Model.model_name == model_name)

    total_results = query.count()
    if total_results == 0:
        raise HTTPException(status_code=404, detail="No Models Found.")

    offset = (page - 1) * page_size
    query = query.offset(offset).limit(page_size)
    results = query.all()

    total_pages = (total_results + page_size - 1) // page_size

    return {
        "total_results": total_results,
        "total_pages": total_pages,
        "page": page,
        "page_size": page_size,
        "data": results
    }