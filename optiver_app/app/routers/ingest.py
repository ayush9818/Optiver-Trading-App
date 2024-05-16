from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import IngestRequest
from app.schema import StockData
from app.crud import get_or_create_date

router = APIRouter()

@router.post("/ingest/")
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
