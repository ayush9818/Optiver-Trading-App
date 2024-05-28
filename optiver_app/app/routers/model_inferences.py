from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from app.database import get_db
from app.models import ModelInferenceCreate, PageModelInference, ModelInferenceRead
from app.schema import ModelInference
from typing import Optional
import logging

# Configure logger
logger = logging.getLogger("optiver." + __name__)

router = APIRouter()


@router.post("/model-inferences/", response_model=ModelInferenceRead)
def create_model_inference(
    model_inference: ModelInferenceCreate, db: Session = Depends(get_db)
):
    """
    Create a new model inference record in the database.

    Args:
        model_inference (ModelInferenceCreate): The model inference data to be created.
        db (Session): Database session dependency.

    Returns:
        ModelInferenceRead: The created model inference record.

    Raises:
        HTTPException: If there is an integrity error or other SQLAlchemy error.
    """
    try:
        # Create a new ModelInference instance from the provided data
        db_model_inference = ModelInference(**model_inference.dict())
        # Add the new record to the session
        db.add(db_model_inference)
        # Commit the transaction to save the record in the database
        db.commit()
        # Refresh the instance to get the generated ID and other fields
        db.refresh(db_model_inference)
        logger.info(f"Created model inference with ID: {db_model_inference.id}")
        return db_model_inference
    except IntegrityError as e:
        # Rollback the transaction in case of an integrity error
        db.rollback()
        logger.warning(f"Integrity error creating model inference: {e}")
        raise HTTPException(
            status_code=400,
            detail="Could not create model inference. Possible duplicate or missing required foreign key.",
        )
    except SQLAlchemyError as e:
        # Rollback the transaction in case of a general SQLAlchemy error
        db.rollback()
        logger.error(f"SQLAlchemy error creating model inference: {e}")
        raise HTTPException(status_code=500, detail="Internal server error.")
    except Exception as e:
        # Rollback the transaction in case of any other exception
        db.rollback()
        logger.error(f"Unexpected error creating model inference: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/model-inferences/", response_model=PageModelInference)
def read_model_inferences(
    model_id: Optional[int] = Query(None, description="Model ID"),
    date_id: Optional[int] = Query(None, description="Date ID"),
    db: Session = Depends(get_db),
    page: int = Query(1, description="Page number"),
    page_size: int = Query(10, description="Number of results per page"),
):
    """
    Retrieve a paginated list of model inferences based on optional filtering criteria.

    Args:
        model_id (Optional[int]): Filter by model ID.
        date_id (Optional[int]): Filter by date ID.
        db (Session): Database session dependency.
        page (int): Page number for pagination.
        page_size (int): Number of results per page for pagination.

    Returns:
        PageModelInference: A paginated response containing the model inferences.

    Raises:
        HTTPException: If no model inferences are found.
    """
    try:
        # Initialize the query on the ModelInference model
        query = db.query(ModelInference)

        # Apply filters if provided
        if model_id is not None:
            query = query.filter(ModelInference.model_id == model_id)
        if date_id is not None:
            query = query.filter(ModelInference.date_id == date_id)

        # Count the total number of results matching the query
        total_results = query.count()

        # Calculate the offset for pagination
        offset = (page - 1) * page_size

        # Apply pagination to the query
        query = query.offset(offset).limit(page_size)

        # Execute the query and retrieve the results
        results = query.all()

        # Raise an HTTPException if no results are found
        if not results:
            logger.warning("No model inferences found.")
            raise HTTPException(status_code=404, detail="No model inferences found.")

        # Calculate the total number of pages
        total_pages = (total_results + page_size - 1) // page_size

        logger.info(
            f"Retrieved {len(results)} model inferences, page {page} of {total_pages}."
        )
        return {
            "total_results": total_results,
            "total_pages": total_pages,
            "page": page,
            "page_size": page_size,
            "data": results,
        }
    except Exception as e:
        logger.error(f"Error retrieving model inferences: {e}")
        raise HTTPException(status_code=500, detail="Internal server error.")
