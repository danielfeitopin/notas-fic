
from pathlib import Path
from app.utils.fetcher import fetch_all_data
from app.utils.fetcher.sources import SOURCES
from app.utils.db.insert_data import insert_data
from app.config import DATA_DIR, FETCH_DATA, CREATE_TABLES
from app.utils.db import create_tables, drop_tables


def main():

    # Create directory for data if it doesn't exist
    Path(DATA_DIR).mkdir(parents=True, exist_ok=True)

    # Fetch data from sources
    if FETCH_DATA:
        fetch_all_data(SOURCES)

    # Insert data into DB
    if CREATE_TABLES:
        print("Inserting data into database...")
        drop_tables()
        create_tables()
        insert_data()


if __name__ == "__main__":

    try:
        main()
    except KeyboardInterrupt:
        print("Process interrupted by user. Exiting...")
        exit(0)
    except Exception as e:
        print(f"An error occurred: {e}")
        exit(1)
