import json

import requests
from requests import Response
from bs4 import BeautifulSoup
from pathlib import Path
from app.config import DATA_DIR
from app.utils.parser import (extract_course_data, extract_subject_results,
                              process_course_data, process_subject_results)

BASE_URL: str = "https://estudos.udc.es/{}/study/quality/{}"


def get_study_url(study_code: str, lang: str = 'gl') -> str:
    return BASE_URL.format(lang, study_code)


def request_data(url: str) -> Response:
    return requests.get(url)


def dump_data(data: dict, filename: Path) -> None:

    file_path: Path = DATA_DIR / filename

    with open(file_path, 'w', encoding='utf-8') as file:
        json.dump(data, file, ensure_ascii=False, indent=4)


def fetch_all_data(sources: dict[str, dict[str, str]]) -> str:

    for source_name, source in sources.items():

        # Fetch data for each year in the source
        for year, url in source.items():

            # Fetch data from the URL
            print(f"Fetching data for {source_name}-{year}...")
            response: Response = request_data(url)
            if response.status_code != 200:
                print(f"Failed to fetch data for {source_name} {year}.")
                continue

            # Parse the response content
            soup: BeautifulSoup = BeautifulSoup(response.text, "html.parser")
            
            # Process and save data
            FILENAME_PREFIX: str = f"{source_name}_{year}"
            if (data := extract_course_data(soup, year)):
                data: dict = process_course_data(data)
                dump_data(data, f"{FILENAME_PREFIX}_course.json")

            if (data := extract_subject_results(soup, year)):
                data: dict = process_subject_results(data)
                dump_data(data, f"{FILENAME_PREFIX}_subject_results.json")

            print(f"Data for {source_name} {year} saved successfully.")
