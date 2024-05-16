from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import StockDataQueryParams, PageRequest, IngestRequest
from app.schema import StockData
from app.utils import clean_nan_values
from app.crud import get_or_create_date

router = APIRouter()

@router.get("/stock_data/", response_model=PageRequest)
def get_stock_data(query_params: StockDataQueryParams = Depends(),
                   db: Session = Depends(get_db),
                   page: int = Query(1, description="Page number"),
                   page_size: int = Query(10, description="Number of results per page")):
    query = db.query(StockData)
    if query_params.start_date_id and query_params.end_date_id:
        query = query.filter(StockData.date_id.between(query_params.start_date_id, query_params.end_date_id))
    elif query_params.date_id:
        query = query.filter(StockData.date_id == query_params.date_id)
    else:
        raise HTTPException(status_code=400, detail="Please provide either a valid date range or valid date id")
    total_results = query.count()
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


@router.post("/stock_data/")
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
