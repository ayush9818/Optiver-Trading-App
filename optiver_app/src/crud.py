import os
from datetime import timedelta, date
from sqlalchemy.orm import Session
from schema import DateMapping 
from models import ModelCreate

def calculate_date_value(db: Session, date_id: int):
    # Find the most recent date_mapping before the given date_id
    recent_date_mapping = (
        db.query(DateMapping)
        .filter(DateMapping.date_id < date_id)
        .order_by(DateMapping.date_id.desc())
        .first()
    )

    if recent_date_mapping:
        days_diff = date_id - recent_date_mapping.date_id
        return recent_date_mapping.date + timedelta(days=days_diff)
    else:
        base_date = date.today() - timedelta(days=os.getenv('NUM_DATE_IDS',480))
        return base_date + timedelta(days=date_id)

def get_or_create_date(db: Session, date_id: int):
    instance = db.query(DateMapping).filter_by(date_id=date_id).one_or_none()
    if instance is None:
        date_value = calculate_date_value(db, date_id)
        instance = DateMapping(date_id=date_id, date=date_value)
        db.add(instance)
        db.commit()
    return instance
