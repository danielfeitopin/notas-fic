from bs4 import BeautifulSoup
import requests
from requests import Response

STUDY_CODES: dict[str, str] = {
    'GEI': '614G01V01',
    'GCED': '614G02V01',
    'GIA': '614G03V01',
}


def request_data(study_code: str, lang: str = 'gl') -> Response:
    url: str = f"https://estudos.udc.es/{lang}/study/quality/{study_code}"
    response: Response = requests.get(url)
    return response


def process_course_data(course_data: BeautifulSoup) -> dict[str, str]:
    processed_data: dict[str, str] = {
        'study_data': {},
        'centre_data': {}
    }

    study_data, centre_data = course_data.find_all(class_='span5')

    # Process study data
    index: int = 0
    for table in study_data.find_all('table'):
        table_body: BeautifulSoup = table.find('tbody')
        for row in table_body.find_all('tr'):
            processed_data['study_data'][f'STUDY_{index}'] = row.find_all(
                'td')[-1].text.strip()
            index += 1

    # Process centre data
    index: int = 0
    for table in centre_data.find_all('table'):
        table_body: BeautifulSoup = table.find('tbody')
        for row in table_body.find_all('tr'):
            processed_data['centre_data'][f'CENTRE_{index}'] = row.find_all(
                'td')[-1].text.strip()
            index += 1

    return processed_data


def process_subject_results(subject_results: BeautifulSoup) -> dict[int, dict]:
    processed_results: dict[int, list] = {}

    # Process subject results
    courses: list = subject_results.find_all(class_='span5')

    for i, course in enumerate(courses):
        processed_results[i+1] = []

        results: BeautifulSoup = course.find(class_='results')
        for subject in results.find_all('dt'):
            subject_name: str = subject.text.strip()
            subject_metrics: BeautifulSoup = subject.find_next_sibling('dd')
            processed_results[i+1].append({
                'name': subject_name,
                'metrics': (
                    subject_metrics.find(class_='bar-success').text.strip(),
                    subject_metrics.find(class_='bar-warning').text.strip(),
                    subject_metrics.find(class_='bar-info').text.strip()
                )
            })

    return processed_results


def process_data(study_data, subject_results) -> dict[str, dict[str, str]]:
    data: dict[str, dict[str, str]] = {}
    data['course_data'] = process_course_data(study_data)
    data['subject_results'] = process_subject_results(subject_results)
    return data
