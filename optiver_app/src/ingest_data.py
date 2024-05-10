import argparse 
import os 
import pandas as pd 
from database import SessionLocal
import logging
import logging.config
from schema import StockData, DateMapping
from utils import get_date_from_date_id

logging.config.fileConfig('configs/logging/local.ini', disable_existing_loggers=False)
logger = logging.getLogger('optiver.'+__name__)


TOTAL_DATE_IDS=481

def get_db():
    db = SessionLocal()
    return db 

def get_or_create_date(args, db, date_id, date_value):
    """Get existing date mapping or create a new one if not exists."""
    date_mapping = db.query(DateMapping).filter_by(date_id=date_id).one_or_none()
    if date_mapping is None:
        date_mapping = DateMapping(date_id=date_id, date=date_value)
        db.add(date_mapping)
        if args.commit:
            db.commit()
    return date_mapping

def get_stock_object(args, db, row):
    date_id = int(row['date_id'])
    date_value = get_date_from_date_id(date_id, TOTAL_DATE_IDS)
    date_mapping = get_or_create_date(args, db, date_id, date_value)
    return StockData(
        stock_id=int(row['stock_id']),
        date_id=int(row['date_id']),
        seconds_in_bucket=int(row['seconds_in_bucket']),
        imbalance_size=float(row['imbalance_size']),
        imbalance_buy_sell_flag=int(row['imbalance_buy_sell_flag']),
        reference_price=float(row['reference_price']),
        matched_size=float(row['matched_size']),
        far_price=float(row['far_price']),
        near_price=float(row['near_price']),
        bid_price=float(row['bid_price']),
        bid_size=float(row['bid_size']),
        ask_price=float(row['ask_price']),
        ask_size=float(row['ask_size']),
        wap=float(row['wap']),
        target=float(row['target']),
        time_id=int(row['time_id']),
        row_id=row['row_id'],
        date_mapping=date_mapping
    )

def ingest_data(args, db, chunk, batch_id):
    data_entries = []   
    try:
        for idx,row in chunk.iterrows():
            stock_data = get_stock_object(args, db, row)
            data_entries.append(stock_data) 
        db.add_all(data_entries)
        if args.commit:
            db.commit()
        logger.info(f"Batch : {batch_id} Ingested Successfully")
    except Exception as e:
        logger.error("An error occurred:", e)
   
if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--data-path", type=str)
    parser.add_argument("--batch-size", type=int, default=500)
    parser.add_argument("--commit", action='store_true',help='if flag provided, then only commit to database')

    args = parser.parse_args()
    data_path = args.data_path
    batch_size = args.batch_size
    logger.info(f"Data Path : {data_path} - Batch Size : {batch_size} - Commit : {args.commit}")

    assert os.path.exists(data_path), f"{data_path} does not exists"
    assert data_path.endswith('.csv'), f"Only csv format is supported"

    chunk_iterator = pd.read_csv(data_path, chunksize=batch_size)
    db = get_db()
    batch_id = 1
    # Process each chunk within a loop
    for chunk in chunk_iterator:
        ingest_data(args, db, chunk, batch_id)
        batch_id+=1
        
# Close the session
db.close()