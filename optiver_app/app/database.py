import warnings

warnings.filterwarnings("ignore")

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import os
from dotenv import load_dotenv
from app.utils import get_secret
import logging

# Configure logger
logger = logging.getLogger("optiver." + __name__)

# Load environment variables from .env file
load_dotenv()
env = os.environ

# Retrieve database secrets from AWS Secrets Manager
logger.info("Retrieving database secrets.")
secrets = get_secret()

# Database connection details
hostname = env.get("DB_HOST")
dbname = env.get("DB_NAME")
port = env.get("DB_PORT")

# Construct the database URL
DATABASE_URL = f"postgresql://{secrets['username']}:{secrets['password']}@{hostname}:{port}/{dbname}"
logger.info(f"Database URL constructed: {DATABASE_URL}")

# Create SQLAlchemy engine
engine = create_engine(DATABASE_URL)
logger.info("SQLAlchemy engine created.")

# Create a configured "Session" class
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
logger.info("SQLAlchemy sessionmaker configured.")


def get_db():
    """
    Dependency that provides a SQLAlchemy session to perform database operations.

    Yields:
        SessionLocal: A SQLAlchemy session.
    """
    logger.info("Creating a new database session.")
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
        logger.info("Database session closed.")
