from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from app.database import get_db
from app.models import ModelInferenceCreate, PageModelInference, ModelInferenceRead
from app.schema import ModelInference

router = APIRouter()

@router.post("/model-inferences/", response_model=ModelInferenceRead)
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

@router.get("/model-inferences/", response_model=PageModelInference)
def read_model_inferences(model_id: int, date_id: int, 
                          db: Session = Depends(get_db),
                          page: int = Query(1, description="Page number"), 
                          page_size: int = Query(10, description="Number of results per page")):
    query = db.query(ModelInference).filter(
        ModelInference.model_id == model_id, 
        ModelInference.date_id == date_id
    )
    total_results = query.count()
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
