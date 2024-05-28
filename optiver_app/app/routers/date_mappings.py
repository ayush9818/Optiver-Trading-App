from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import DateMappingQueryParams, PageDateRequest
from app.schema import DateMapping
from app.utils import apply_filters
import logging

# Configure logger
logger = logging.getLogger("optiver." + __name__)

router = APIRouter()


@router.get("/date_mappings/", response_model=PageDateRequest)
def get_date_mappings(
    query_params: DateMappingQueryParams = Depends(),
    db: Session = Depends(get_db),
    page: int = Query(1, description="Page number"),
    page_size: int = Query(10, description="Number of results per page"),
):
    """
    Retrieve a paginated list of date mappings based on the provided query parameters.

    Args:
        query_params (DateMappingQueryParams): Query parameters for filtering date mappings.
        db (Session): Database session dependency.
        page (int): Page number for pagination.
        page_size (int): Number of results per page for pagination.

    Returns:
        PageDateRequest: A paginated response containing the date mappings.

    Raises:
        HTTPException: If no date mappings are found matching the criteria.
    """
    try:
        # Convert query parameters to dictionary, excluding any None values
        query_params = query_params.dict(exclude_none=True)

        # Initialize query on the DateMapping model
        query = db.query(DateMapping)

        # Apply filters to the query based on the provided query parameters
        query = apply_filters(query, DateMapping, query_params)

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
            logger.warning("No date mappings found matching the criteria.")
            raise HTTPException(
                status_code=404, detail="No date mappings found matching the criteria."
            )

        # Calculate the total number of pages
        total_pages = (total_results + page_size - 1) // page_size

        logger.info(
            f"Retrieved {len(results)} date mappings, page {page} of {total_pages}."
        )
        return {
            "total_results": total_results,
            "total_pages": total_pages,
            "page": page,
            "page_size": page_size,
            "data": results,
        }
    except Exception as e:
        logger.error(f"Error retrieving date mappings: {e}")
        raise HTTPException(status_code=500, detail="Internal server error.")
