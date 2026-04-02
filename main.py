import os
from pathlib import Path
from dotenv import load_dotenv
from sqlalchemy import create_engine


load_dotenv()

# Create "database" folder if it doesn't exist
db_folder = Path('database')
db_folder.mkdir(exist_ok=True)

# Try to retrieve 'DATABASE_URL' from .env file
database_url = os.getenv('DATABASE_URL')
if not database_url:
    raise ValueError('DATABASE_URL is missing from the .env file.')

engine = create_engine(database_url, echo=True)

with engine.connect():
    pass
