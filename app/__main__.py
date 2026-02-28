import json
from bs4 import BeautifulSoup
from pathlib import Path
from requests import Response
from app.utils.fetcher import fetch_all_data
from app.utils.fetcher.sources import SOURCES
from app.utils.db.insert_data import insert_data_into_db
from app.utils.studies import STUDY_CODES
from app.config import DATA_DIR, FETCH_DATA


def main():

    # Create directory for data if it doesn't exist
    Path(DATA_DIR).mkdir(parents=True, exist_ok=True)

    # Fetch data from sources
    if FETCH_DATA:
        fetch_all_data(SOURCES)

    # Insert data into DB
    # print("Inserting data into database...")
    # insert_data_into_db(YEAR, STUDY_CODE, data)
    # print("Data insertion completed successfully.")


if __name__ == "__main__":

    STUDY_CODE: str = STUDY_CODES.get('GCED', '')
    YEAR: str = '2024'
    LANG: str = 'gl'

    try:
        main()
    except KeyboardInterrupt:
        print("Process interrupted by user. Exiting...")
        exit(0)
    except Exception as e:
        print(f"An error occurred: {e}")
        exit(1)
