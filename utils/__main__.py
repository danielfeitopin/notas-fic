from bs4 import BeautifulSoup
from .parser import request_data, process_data
from .insert_data import insert_data_into_db
from .studies import STUDY_CODES

def main():

    # Retrieve data
    print(f"Requesting data for study code {STUDY_CODE} and year {YEAR}...")
    html: str = request_data(STUDY_CODE, LANG).text

    if html:

        # Parse HTML
        print("Data retrieved successfully. Parsing HTML...")
        if not (soup := BeautifulSoup(html, features="html.parser")):
            raise ValueError("Failed to parse HTML content.")

        # Extract course data
        print("Extracting course data...")
        if not (course_data := soup.find(id=f'curse{YEAR}')):
            print(f"Failed to extract course data for year {YEAR}.")

        # Extract subject results
        print("Extracting subject results...")
        if not (subject_results := soup.find(id=f'detailedresults{YEAR}')):
            print(f"Failed to extract subject results for year {YEAR}.")

        # Process data
        print("Processing data...")
        data: dict[str, dict[str, str]] = process_data(
            course_data, subject_results)
        
        # Insert data into DB
        print("Inserting data into database...")
        insert_data_into_db(YEAR, STUDY_CODE, data)
        print("Data insertion completed successfully.")


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