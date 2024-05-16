from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import DateMappingQueryParams, PageDateRequest
from app.schema import DateMapping
from app.utils import apply_filters

router = APIRouter()

@router.get("/date_mappings/", response_model=PageDateRequest)
def get_date_mappings(query_params: DateMappingQueryParams = Depends(),
                      db: Session = Depends(get_db),
                      page: int = Query(1, description="Page number"),
                      page_size: int = Query(10, description="Number of results per page")):
    query_params = query_params.dict(exclude_none=True)
    query = db.query(DateMapping)
    query = apply_filters(query, DateMapping, query_params)
    total_results = query.count()
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
