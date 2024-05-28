import argparse
import os
import pandas as pd
from database import SessionLocal
import logging
import logging.config
from app.schema import StockData, DateMapping
from app.utils import get_date_from_date_id

# Configure logger
logging.config.fileConfig(
    "app/configs/logging/local.ini", disable_existing_loggers=False
)
logger = logging.getLogger("optiver." + __name__)

TOTAL_DATE_IDS = 481


def get_db():
    """
    Create and return a new database session.

    Returns:
        SessionLocal: A SQLAlchemy session.
    """
    logger.info("Creating a new database session.")
    db = SessionLocal()
    return db


def get_or_create_date(args, db, date_id, date_value):
    """
    Get existing date mapping or create a new one if it does not exist.

    Args:
        args (Namespace): Command line arguments.
        db (Session): Database session.
        date_id (int): The date ID.
        date_value (date): The date value.

    Returns:
        DateMapping: The date mapping instance.
    """
    logger.debug(f"Getting or creating date mapping for date_id: {date_id}.")
    date_mapping = db.query(DateMapping).filter_by(date_id=date_id).one_or_none()
    if date_mapping is None:
        date_mapping = DateMapping(date_id=date_id, date=date_value)
        db.add(date_mapping)
        if args.commit:
            db.commit()
            logger.info(
                f"New date mapping created and committed for date_id: {date_id}."
            )
    return date_mapping


def get_stock_object(args, db, row):
    """
    Create a StockData object from a row of data.

    Args:
        args (Namespace): Command line arguments.
        db (Session): Database session.
        row (Series): A row of data from the CSV file.

    Returns:
        StockData: A StockData instance.
    """
    logger.debug("Creating StockData object from row.")
    date_id = int(row["date_id"])
    date_value = get_date_from_date_id(date_id, TOTAL_DATE_IDS)
    date_mapping = get_or_create_date(args, db, date_id, date_value)
    return StockData(
        stock_id=int(row["stock_id"]),
        date_id=int(row["date_id"]),
        seconds_in_bucket=int(row["seconds_in_bucket"]),
        imbalance_size=float(row["imbalance_size"]),
        imbalance_buy_sell_flag=int(row["imbalance_buy_sell_flag"]),
        reference_price=float(row["reference_price"]),
        matched_size=float(row["matched_size"]),
        far_price=float(row["far_price"]),
        near_price=float(row["near_price"]),
        bid_price=float(row["bid_price"]),
        bid_size=float(row["bid_size"]),
        ask_price=float(row["ask_price"]),
        ask_size=float(row["ask_size"]),
        wap=float(row["wap"]),
        target=float(row["target"]),
        time_id=int(row["time_id"]),
        row_id=row["row_id"],
        date_mapping=date_mapping,
    )


def ingest_data(args, db, chunk, batch_id):
    """
    Ingest a chunk of data into the database.

    Args:
        args (Namespace): Command line arguments.
        db (Session): Database session.
        chunk (DataFrame): A chunk of data from the CSV file.
        batch_id (int): The batch ID.
    """
    logger.info(f"Ingesting batch: {batch_id}.")
    data_entries = []
    try:
        for idx, row in chunk.iterrows():
            stock_data = get_stock_object(args, db, row)
            data_entries.append(stock_data)
        db.add_all(data_entries)
        if args.commit:
            db.commit()
            logger.info(f"Batch {batch_id} ingested and committed successfully.")
    except Exception as e:
        logger.error(f"An error occurred while ingesting batch {batch_id}: {e}")
        db.rollback()


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--data-path",
        type=str,
        required=True,
        help="Path to the CSV file containing the data.",
    )
    parser.add_argument(
        "--batch-size",
        type=int,
        default=500,
        help="Number of rows to process in each batch.",
    )
    parser.add_argument(
        "--commit",
        action="store_true",
        help="If provided, commit the data to the database.",
    )

    args = parser.parse_args()
    data_path = args.data_path
    batch_size = args.batch_size
    logger.info(
        f"Data Path: {data_path}, Batch Size: {batch_size}, Commit: {args.commit}"
    )

    # Ensure the provided data path exists and is a CSV file
    assert os.path.exists(data_path), f"{data_path} does not exist."
    assert data_path.endswith(".csv"), "Only CSV format is supported."

    chunk_iterator = pd.read_csv(data_path, chunksize=batch_size)
    db = get_db()
    batch_id = 1

    # Process each chunk within a loop
    for chunk in chunk_iterator:
        ingest_data(args, db, chunk, batch_id)
        batch_id += 1

    # Close the session
    db.close()
    logger.info("Database session closed.")
