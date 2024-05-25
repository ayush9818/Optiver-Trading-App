# Suppressing unnecessary warnings
import warnings
warnings.filterwarnings("ignore")

import argparse
import logging
import logging.config
from sqlalchemy import Column, Integer, Float, String, Date, ForeignKey, JSON
from sqlalchemy.orm import relationship, backref
from app.base import Base

# Configure logger
logging.config.fileConfig('app/configs/logging/local.ini', disable_existing_loggers=False)
logger = logging.getLogger('optiver.' + __name__)

class StockData(Base):
    """
    Represents stock data for trading with detailed market metrics.

    Attributes:
        id (int): Primary key, auto-incremented.
        stock_id (int): Identifier for the stock.
        date_id (int): Foreign key linking to date_mapping.
        seconds_in_bucket (int): Number of seconds in the bucket.
        imbalance_size (float): Size of the imbalance.
        imbalance_buy_sell_flag (int): Flag indicating buy or sell imbalance.
        reference_price (float): Reference price of the stock.
        matched_size (float): Size of matched orders.
        far_price (float): Far price of the stock.
        near_price (float): Near price of the stock.
        bid_price (float): Bid price of the stock.
        bid_size (float): Bid size of the stock.
        ask_price (float): Ask price of the stock.
        ask_size (float): Ask size of the stock.
        wap (float): Weighted average price.
        target (float): Target price.
        time_id (int): Time identifier.
        train_type (str): Type of training.
        row_id (str): Row identifier, primary key.
        date_mapping (DateMapping): Relationship to DateMapping.
    """
    
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
    date_mapping = relationship('DateMapping', backref=backref('stock_data', cascade="all, delete-orphan"))

class DateMapping(Base):
    """
    Links date IDs to actual dates and associated stock data.

    Attributes:
        date_id (int): Unique identifier for each date.
        date (Date): The actual date.
    """
    
    __tablename__ = 'date_mapping'
    date_id = Column(Integer, primary_key=True)
    date = Column(Date, nullable=False)

class TrainingSession(Base):
    """
    Stores information about model training sessions, including associated stock data.

    Attributes:
        training_session_id (int): Primary key, auto-incremented.
        model_id (int): Foreign key linking to model.
        date_id (int): Foreign key linking to date_mapping.
        stock_ids (JSON): JSON list of stock IDs used in the training session.
        date_mapping (DateMapping): Relationship to DateMapping.
        model (Model): Relationship to Model.
    """
    
    __tablename__ = 'training_session'
    training_session_id = Column(Integer, primary_key=True, autoincrement=True)
    model_id = Column(Integer, ForeignKey('model.model_id'), nullable=False)
    date_id = Column(Integer, ForeignKey('date_mapping.date_id'))
    stock_ids = Column(JSON)
    date_mapping = relationship("DateMapping", backref=backref("training_session", cascade="all, delete-orphan"))
    model = relationship("Model", backref=backref("training_session", cascade="all, delete-orphan"))

class Model(Base):
    """
    Represents a machine learning model with metadata.

    Attributes:
        model_id (int): Primary key, auto-incremented.
        model_name (str): Name of the model.
        model_artifact_path (str): Path to the model artifact.
        date_id (int): Foreign key linking to date_mapping.
        date_mapping (DateMapping): Relationship to DateMapping.
    """
    
    __tablename__ = 'model'
    model_id = Column(Integer, primary_key=True, autoincrement=True)
    model_name = Column(String(255), nullable=False)
    model_artifact_path = Column(String(255), nullable=False)
    date_id = Column(Integer, ForeignKey('date_mapping.date_id'), nullable=False)
    date_mapping = relationship("DateMapping", backref=backref("Model", cascade="all, delete-orphan"))

class ModelInference(Base):
    """
    Stores inferences made by a model.

    Attributes:
        id (int): Primary key, auto-incremented.
        model_id (int): Foreign key linking to model.
        date_id (int): Foreign key linking to date_mapping.
        predictions (str): Predictions made by the model.
        model (Model): Relationship to Model.
        date_mapping (DateMapping): Relationship to DateMapping.
    """
    
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
        logger.info("DB Schema created successfully.")
