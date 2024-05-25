from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from app.database import get_db
from app.models import ModelCreate, PageModelRequest
from app.schema import Model
from typing import Optional
import logging

# Configure logger
logger = logging.getLogger('optiver.' + __name__)

router = APIRouter()

@router.post("/models/")
async def create_model(model: ModelCreate, db: Session = Depends(get_db)):
    """
    Create a new model record in the database.

    Args:
        model (ModelCreate): The model data to be created.
        db (Session): Database session dependency.

    Returns:
        dict: A message indicating the model was created successfully.

    Raises:
        HTTPException: If a model with the same name already exists.
    """
    logger.info("Attempting to create a new model.")
    # Check if a model with the same name already exists
    existing_model = db.query(Model).filter(Model.model_name == model.model_name).first()
    if existing_model:
        logger.warning(f"Model with name {model.model_name} already exists.")
        raise HTTPException(status_code=400, detail="Model already exists")
    
    # Create a new Model instance
    new_model = Model(model_name=model.model_name, model_artifact_path=model.model_artifact_path, date_id=model.date_id)
    db.add(new_model)
    try:
        # Commit the transaction to save the record in the database
        db.commit()
        logger.info(f"Model {model.model_name} created successfully.")
    except IntegrityError:
        # Rollback the transaction in case of an integrity error
        db.rollback()
        logger.error(f"Integrity error creating model {model.model_name}.")
        raise HTTPException(status_code=400, detail="Model with this name already exists")
    
    # Refresh the instance to get the generated ID and other fields
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
    """
    Retrieve a paginated list of models based on optional filtering criteria.

    Args:
        model_id (Optional[int]): Filter by model ID.
        model_name (Optional[str]): Filter by model name.
        page (int): Page number for pagination.
        page_size (int): Number of results per page for pagination.
        db (Session): Database session dependency.

    Returns:
        PageModelRequest: A paginated response containing the models.

    Raises:
        HTTPException: If no models are found.
    """
    logger.info("Reading models with provided filters.")
    # Initialize the query on the Model model
    query = db.query(Model)

    # Apply filters if provided
    if model_id is not None:
        query = query.filter(Model.model_id == model_id)
    elif model_name is not None:
        query = query.filter(Model.model_name == model_name)

    # Count the total number of results matching the query
    total_results = query.count()
    if total_results == 0:
        logger.warning("No models found matching the criteria.")
        raise HTTPException(status_code=404, detail="No Models Found.")

    # Calculate the offset for pagination
    offset = (page - 1) * page_size

    # Apply pagination to the query
    query = query.offset(offset).limit(page_size)

    # Execute the query and retrieve the results
    results = query.all()

    # Calculate the total number of pages
    total_pages = (total_results + page_size - 1) // page_size

    logger.info(f"Retrieved {len(results)} models, page {page} of {total_pages}.")
    return {
        "total_results": total_results,
        "total_pages": total_pages,
        "page": page,
        "page_size": page_size,
        "data": results
    }
