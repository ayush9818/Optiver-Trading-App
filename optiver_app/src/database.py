import warnings
warnings.filterwarnings("ignore")

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import os
from dotenv import load_dotenv
from utils import get_secret

load_dotenv()
env = os.environ

secrets = get_secret()
hostname = env.get('DB_HOST')
dbname = env.get('DB_NAME')
port = env.get('DB_PORT')


DATABASE_URL = f"postgresql://{secrets['username']}:{secrets['password']}@{hostname}:{port}/{dbname}"
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)