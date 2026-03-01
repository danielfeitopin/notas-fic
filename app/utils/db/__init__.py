from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from app.config import DB_PATH
from .model import Base

ENGINE = create_engine(DB_PATH)
SESSION: Session = sessionmaker(bind=ENGINE)


def create_tables():
    """Creates the tables in the database based on the defined models."""

    Base.metadata.create_all(ENGINE)

    # Show created tables
    for table in Base.metadata.tables:
        print(f"Táboa creada: {table}")

def drop_tables():
    """Drops all tables in the database."""

    Base.metadata.drop_all(ENGINE)

    # Show dropped tables
    for table in Base.metadata.tables:
        print(f"Táboa eliminada: {table}")