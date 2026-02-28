from bs4 import BeautifulSoup


def extract_course_data(soup: BeautifulSoup, year: str) -> BeautifulSoup:
    return soup.find(id=f'curse{year}')


def extract_subject_results(soup: BeautifulSoup, year: str) -> BeautifulSoup:
    return soup.find(id=f'detailedresults{year}')


def process_data(data: BeautifulSoup) -> dict[str, str]:
    processed_data: dict[str, str] = {}

    index: int = 0
    for table in data.find_all('table'):
        table_body: BeautifulSoup = table.find('tbody')
        for row in table_body.find_all('tr'):
            processed_data[index] = row.find_all(
                'td')[-1].text.strip()
            index += 1

    return processed_data


def process_course(course_data: BeautifulSoup) -> dict[str, dict[str, str]]:

    study_data, centre_data = course_data.find_all(class_='span5')
    processed_data: dict[str, dict[str, str]] = {
        'study_data': process_data(study_data),
        'centre_data': process_data(centre_data)
    }

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
