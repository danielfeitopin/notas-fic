from . import get_study_url
from app.utils.studies import STUDY_CODES


GEI_SOURCES: dict[str, str] = {

}

GCED_SOURCES: dict[str, str] = {
    '2019': f'https://web.archive.org/web/20220927180421/{get_study_url(STUDY_CODES["GCED"])}',
    '2020': f'https://web.archive.org/web/20220927180421/{get_study_url(STUDY_CODES["GCED"])}',
    '2021': f'https://web.archive.org/web/20240624133932/{get_study_url(STUDY_CODES["GCED"])}',
    '2022': f'https://web.archive.org/web/20250713210734/{get_study_url(STUDY_CODES["GCED"])}',
    '2023': f'https://web.archive.org/web/20250713210734/{get_study_url(STUDY_CODES["GCED"])}',
    '2024': get_study_url(STUDY_CODES["GCED"]),
    '2025': get_study_url(STUDY_CODES["GCED"]),
}

GIA_SOURCES: dict[str, str] = {

}

SOURCES: dict[str, dict[str, str]] = {
    'GEI': GEI_SOURCES,
    'GCED': GCED_SOURCES,
    'GIA': GIA_SOURCES
}
