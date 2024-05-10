# Suppressing unnecessary warnings
import warnings
warnings.filterwarnings("ignore")

import argparse
import logging
import logging.config
from sqlalchemy import Column, Integer, Float, String, Date, ForeignKey, JSON, Boolean
from sqlalchemy.orm import relationship, backref
from base import Base

logging.config.fileConfig('configs/logging/local.ini', disable_existing_loggers=False)
logger = logging.getLogger('optiver.'+__name__)

class StockData(Base):
    """Represents stock data for trading with detailed market metrics."""
    
    __tablename__ = 'stock_data'
    id = Column(Integer, primary_key=True, autoincrement=True)
    stock_id = Column(Integer, nullable=False)
    date_id = Column(Integer, ForeignKey('date_mapping.date_id', ondelete="CASCADE"), index=True) 
    seconds_in_bucket = Column(Integer)
    imbalance_size = Column(Float)
    imbalance_buy_sell_flag = Column(Integer)
    reference_price = Column(Float)
    matched_size = Column(Float)
    far_price = Column(Float)
    near_price = Column(Float)
    bid_price = Column(Float)
    bid_size = Column(Float)
    ask_price = Column(Float)
    ask_size = Column(Float)
    wap = Column(Float)
    target = Column(Float)
    time_id = Column(Integer)
    train_type = Column(String(20))
    row_id = Column(String(20), primary_key=True)
    date_mapping = relationship('DateMapping', backref=backref('stock_data',cascade="all, delete-orphan"))

class DateMapping(Base):
    """Links date IDs to actual dates and associated stock data."""

    __tablename__ = 'date_mapping'
    date_id = Column(Integer, primary_key=True)  # Unique identifier for each date
    date = Column(Date, nullable=False)

class TrainingSession(Base):
    """Stores information about model training sessions, including associated stock data."""

    __tablename__ = 'training_session'
    training_session_id = Column(Integer, primary_key=True)
    model_id = Column(Integer, ForeignKey('model.model_id'), nullable=False)
    date_id = Column(Integer, ForeignKey('date_mapping.date_id'))
    stock_ids = Column(JSON)
    date_mapping = relationship("DateMapping", backref=backref("training_session", cascade="all, delete-orphan"))
    model = relationship("Model", backref=backref("training_session", cascade="all, delete-orphan"))

class Model(Base):
    __tablename__ = 'model'
    model_id = Column(Integer, primary_key=True)
    model_name = Column(String(255), nullable=False)
    model_artifact_path = Column(String(255), nullable=False)

class ModelInference(Base):
    __tablename__ = "model_inference"
    id = Column(Integer, primary_key=True, autoincrement=True)
    model_id = Column(Integer, ForeignKey('model.model_id'), nullable=False)
    date_id = Column(Integer, ForeignKey('date_mapping.date_id'), nullable=False)
    predictions = Column(String(255), nullable=False)
    model = relationship("Model", backref=backref("model_inference", cascade="all, delete-orphan"))
    date_mapping = relationship("DateMapping", backref=backref("model_inference", cascade="all, delete-orphan"))

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--create-schema', action='store_true', help='Create DB Schema')

    args = parser.parse_args()
    if args.create_schema:
        logger.info("Creating DB Schema")
        from database import engine 
        Base.metadata.create_all(bind=engine)

