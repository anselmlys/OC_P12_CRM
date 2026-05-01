import os
from pathlib import Path
from dotenv import load_dotenv
from sqlalchemy import create_engine, event
from sqlalchemy.orm import sessionmaker


load_dotenv()

# Create "database" folder if it doesn't exist
db_folder = Path('database')
db_folder.mkdir(exist_ok=True)

# Try to retrieve 'DATABASE_URL' from .env file
database_url = os.getenv('DATABASE_URL')
if not database_url:
    raise ValueError('DATABASE_URL is missing from the .env file.')

engine = create_engine(database_url, echo=False)


# Ensure SQLite enforces foreign key constraints for every new connection
@event.listens_for(engine, 'connect')
def enable_sqlite_foreign_key(dbapi_connection, connection_record):
    dbapi_connection.execute('PRAGMA foreign_keys=ON')


Session = sessionmaker(bind=engine)
