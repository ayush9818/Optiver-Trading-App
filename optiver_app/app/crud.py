import os
from datetime import timedelta, date
from sqlalchemy.orm import Session
from app.schema import DateMapping
from app.models import ModelCreate
import logging

# Configure logger
logger = logging.getLogger("optiver." + __name__)


def calculate_date_value(db: Session, date_id: int) -> date:
    """
    Calculate the date value for a given date_id.

    Args:
        db (Session): The database session.
        date_id (int): The date ID for which to calculate the date value.

    Returns:
        date: The calculated date value.
    """
    logger.info(f"Calculating date value for date_id: {date_id}.")

    # Find the most recent date_mapping before the given date_id
    recent_date_mapping = (
        db.query(DateMapping)
        .filter(DateMapping.date_id < date_id)
        .order_by(DateMapping.date_id.desc())
        .first()
    )

    if recent_date_mapping:
        # Calculate the difference in days and return the new date
        days_diff = date_id - recent_date_mapping.date_id
        calculated_date = recent_date_mapping.date + timedelta(days=days_diff)
        logger.info(f"Found recent date mapping. Calculated date: {calculated_date}.")
        return calculated_date
    else:
        # Calculate the base date from today minus a configured number of days
        base_date = date.today() - timedelta(days=int(os.getenv("NUM_DATE_IDS", 480)))
        calculated_date = base_date + timedelta(days=date_id)
        logger.info(
            f"No recent date mapping found. Calculated base date: {calculated_date}."
        )
        return calculated_date


def get_or_create_date(db: Session, date_id: int) -> DateMapping:
    """
    Retrieve or create a DateMapping instance for a given date_id.

    Args:
        db (Session): The database session.
        date_id (int): The date ID for which to retrieve or create the DateMapping.

    Returns:
        DateMapping: The retrieved or newly created DateMapping instance.
    """
    logger.info(f"Getting or creating date mapping for date_id: {date_id}.")

    # Check if the DateMapping instance already exists
    instance = db.query(DateMapping).filter_by(date_id=date_id).one_or_none()
    if instance is None:
        # Calculate the date value and create a new DateMapping instance
        date_value = calculate_date_value(db, date_id)
        instance = DateMapping(date_id=date_id, date=date_value)
        db.add(instance)
        db.commit()
        logger.info(
            f"Created new date mapping for date_id: {date_id}, date: {date_value}."
        )
    else:
        logger.info(
            f"Found existing date mapping for date_id: {date_id}, date: {instance.date}."
        )

    return instance
