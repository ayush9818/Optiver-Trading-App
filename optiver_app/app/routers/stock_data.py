from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import StockDataQueryParams, PageRequest, IngestRequest
from app.schema import StockData
from app.utils import clean_nan_values
from app.crud import get_or_create_date
import logging

# Configure logger
logger = logging.getLogger('optiver.' + __name__)

router = APIRouter()

@router.get("/stock_data/", response_model=PageRequest)
def get_stock_data(query_params: StockDataQueryParams = Depends(),
                   db: Session = Depends(get_db),
                   page: int = Query(1, description="Page number"),
                   page_size: int = Query(10, description="Number of results per page")):
    """
    Retrieve a paginated list of stock data based on the provided query parameters.

    Args:
        query_params (StockDataQueryParams): Query parameters for filtering stock data.
        db (Session): Database session dependency.
        page (int): Page number for pagination.
        page_size (int): Number of results per page for pagination.

    Returns:
        PageRequest: A paginated response containing the stock data.

    Raises:
        HTTPException: If no stock data is found or if query parameters are invalid.
    """
    logger.info("Fetching stock data with provided filters.")
    
    # Initialize query on the StockData model
    query = db.query(StockData)
    
    # Apply filters based on query parameters
    if query_params.start_date_id and query_params.end_date_id:
        query = query.filter(StockData.date_id.between(query_params.start_date_id, query_params.end_date_id))
    elif query_params.date_id:
        query = query.filter(StockData.date_id == query_params.date_id)
    else:
        logger.warning("Invalid query parameters: Either date range or date id must be provided.")
        raise HTTPException(status_code=400, detail="Please provide either a valid date range or valid date id")
    
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
        logger.warning("No stock data found matching the criteria.")
        raise HTTPException(status_code=404, detail="No stock data found matching the criteria.")
    
    # Clean NaN values from results
    cleaned_results = [clean_nan_values(result.__dict__) for result in results]
    
    # Calculate the total number of pages
    total_pages = (total_results + page_size - 1) // page_size
    
    logger.info(f"Retrieved {len(results)} stock data records, page {page} of {total_pages}.")
    return {
        "total_results": total_results,
        "total_pages": total_pages,
        "page": page,
        "page_size": page_size,
        "data": cleaned_results
    }

@router.post("/stock_data/")
async def ingest_data(request: IngestRequest, db: Session = Depends(get_db)):
    """
    Ingest new stock data records into the database.

    Args:
        request (IngestRequest): The request containing stock data to be ingested.
        db (Session): Database session dependency.

    Returns:
        dict: A message indicating the data was ingested successfully.

    Raises:
        HTTPException: If there is an error during ingestion.
    """
    logger.info("Ingesting new stock data.")
    try:
        # Iterate over each data item in the request
        for item in request.data:
            # Get or create the date mapping
            date_mapping = get_or_create_date(db, item.date_id)
            # Add the new stock data record to the session
            db.add(StockData(**item.dict(), date_mapping=date_mapping))
        
        # Commit the transaction if specified in the request
        if request.commit:
            db.commit()
            logger.info("Stock data committed to the database.")
        
        return {"message": "Data ingested successfully."}
    except Exception as e:
        # Rollback the transaction in case of an error
        db.rollback()
        logger.error(f"Error ingesting data: {e}")
        raise HTTPException(status_code=500, detail=str(e))
