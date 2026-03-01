# SPDX-FileCopyrightText: 2026 Daniel Feito-Pin <danielfeitopin+github@protonmail.com>
#
# SPDX-License-Identifier: GPL-3.0-or-later

import json
from pathlib import Path
from sqlalchemy.orm import Session
from . import SESSION
from . import model
from app.config import DATA_DIR
from app.utils.studies import STUDY_NAMES, STUDY_ACRONYMS, STUDY_CODES

RATE_TYPES = ["study_data", "centre_data"]

RATE_CATEGORIES = [
    "Matriculación de estudantes",
    "Matriculación en créditos",
    "Resultados académicos",
    "Taxas SEGUIMENTO",
]

RATE_NAMES = [
    "Número de estudantes",
    "Homes",
    "Mulleres",
    "Total de créditos matriculados",
    "Créditos en 1ª matrícula",
    "Créditos en 2ª matrícula",
    "Créditos en 3ª e sucesivas matrículas",
    "% créditos repetidos",
    "Media de créditos por estudante",
    "Taxa de evaluación",
    "Taxa de éxito",
    "Taxa de rendemento",
    "Taxa de eficiencia",
    "Taxa de graduación",
    "Taxa de abandono",
]

STUDY_RATE_DICT: list[tuple[str, str]] = [
    (RATE_NAMES[i], RATE_CATEGORIES[j])
    for i, j in enumerate([0] * 3 + [1] * 6 + [2] * 6)
]

CENTRE_RATE_DICT: list[tuple[str, str]] = [
    (RATE_NAMES[i], RATE_CATEGORIES[j])
    for i, j in enumerate([0] * 3 + [1] * 6 + [2] * 3)
]


def list_input_files(data_dir: str = DATA_DIR) -> list[str]:
    """Get list of all files in the data directory"""
    return [file.name for file in Path(data_dir).glob("*.json")]


def group_files_by_type(filenames: list[str]) -> dict[str, list[str]]:

    groups: dict[str, list[str]] = {
        'centre_data': [],
        'study_data': [],
        'subject_results': []
    }

    for name in filenames:
        name_parts: list[str] = name.split('_')
        if name_parts[0] == 'FIC':
            groups['centre_data'].append(name)
        elif name_parts[-1] == 'study.json':
            groups['study_data'].append(name)
        elif name_parts[-1] == 'results.json':
            groups['subject_results'].append(name)
        else:
            print(f"Unknown file type for {name}, skipping...")

    return groups


def group_files_by_study(filenames: list[str]) -> dict[str, list[str]]:

    groups: dict[str, list[str]] = {
        'GEI': [],
        'GCED': [],
        'GIA': []
    }

    for name in filenames:
        name_parts: list[str] = name.split('_')
        if name_parts[0] in {'GEI', 'GCED', 'GIA'}:
            groups[name_parts[0]].append(name)
        else:
            print(f"Unknown study code in filename: {name}, skipping...")

    return groups


def get_year_from_filename(filename: str) -> int:
    """Extract the year from a filename'"""
    return int(filename.split('_')[1])


def load_json_data(filename: str) -> dict:
    """Load JSON data from a file in the data directory"""
    with open(Path(DATA_DIR) / filename, 'r', encoding='utf-8') as f:
        return json.load(f)


def insert_into_Carreira(session: Session):
    for study_code, study_acronym in STUDY_ACRONYMS.items():

        # Check if already exists
        existing_carreira = session.query(model.Carreira).filter_by(
            codigo=study_code
        ).first()

        if existing_carreira:
            print(f"Carreira already exists: {study_code}")
            continue

        session.add(
            model.Carreira(
                codigo=study_code,
                nome=STUDY_NAMES[study_code],
                siglas=study_acronym
            )
        )


def insert_into_Anoacademico(session: Session, first_year: int, last_year: int):
    for year in range(first_year, last_year + 1):

        # Check if already exists
        existing_year = session.query(model.Anoacademico).filter_by(
            codigo=f'{year}/{year + 1}'
        ).first()

        if existing_year:
            print(f"Anoacademico already exists: {year}")
            continue

        session.add(
            model.Anoacademico(
                codigo=f'{year}/{year + 1}',
                inicio=year,
                fin=year + 1
            )
        )
        print(f"Inserted Anoacademico: {year}/{year + 1}")


def insert_into_TaxaCentro(session: Session):
    for rate_name, rate_category in CENTRE_RATE_DICT:

        # Check if already exists
        existing_rate = session.query(model.Taxacentro).filter_by(
            nome=rate_name,
            categoria=rate_category
        ).first()

        if existing_rate:
            print(f"Rate already exists: {rate_name} in 'TaxaCentro'")
            continue

        session.add(
            model.Taxacentro(
                codigo=CENTRE_RATE_DICT.index((rate_name, rate_category)),
                nome=rate_name,
                categoria=rate_category
            )
        )


def insert_into_TaxaEstudo(session: Session):
    for rate_name, rate_category in STUDY_RATE_DICT:
        for study_code in STUDY_ACRONYMS:

            # Check if already exists
            existing_rate = session.query(model.Taxaestudo).filter_by(
                nome=rate_name,
                categoria=rate_category,
                codigo_carreira=study_code
            ).first()

            if existing_rate:
                print(f"Rate already exists: {rate_name} in 'TaxaEstudo'")
                continue

            session.add(
                model.Taxaestudo(
                    codigo=STUDY_RATE_DICT.index((rate_name, rate_category)),
                    nome=rate_name,
                    categoria=rate_category,
                    codigo_carreira=study_code
                )
            )


def insert_into_Asignatura(session: Session, study_code: str, results: dict):
    for course in results:
        for subject in results[course]:
            subject_name: str = subject['name']

            # Check if already exists
            existing_subject = session.query(model.Asignatura).filter_by(
                nome=subject_name,
                codigo_carreira=study_code
            ).first()

            if existing_subject:
                continue

            new_subject = model.Asignatura(
                codigo=str(session.query(model.Asignatura).count() + 1),
                codigo_carreira=study_code,
                nome=subject_name,
                curso=int(course)
            )

            session.add(new_subject)


def insert_into_Cursase(session: Session, year: int, study_code: str, results: dict):
    for course in results:
        for subject in results[course]:
            subject_name: str = subject['name']
            passed, failed, np = map(int, subject['metrics'])

            # Check if already exists
            existing_subject = session.query(model.Asignatura).filter_by(
                nome=subject_name,
                codigo_carreira=study_code
            ).first()

            if not existing_subject:
                continue

            new_cursase = model.Cursase(
                codigo_anoacademico=f'{year}/{year + 1}',
                codigo_asignatura=existing_subject.codigo,
                aprobados=passed,
                suspensos=failed,
                np=np
            )

            session.add(new_cursase)


def process_results_data(session: Session, filenames: list[str]):

    # Process each study group separately
    groups: dict[str, list[str]] = group_files_by_study(filenames)
    for study, study_filenames in groups.items():

        # Process each file for the study
        for filename in study_filenames:
            results_data: dict = load_json_data(filename)

            print(f"Processing results data for {filename}...")
            insert_into_Asignatura(session, STUDY_CODES[study], results_data)
            year = get_year_from_filename(filename)
            insert_into_Cursase(
                session, year, STUDY_CODES[study], results_data)


def insert_data():

    # Initialize database session
    session: Session = SESSION()

    # Insert data into 'Carreira'
    print("Inserting data into 'Carreira'...")
    insert_into_Carreira(session)

    # Insert data into 'Taxacentro'
    print("Inserting data into 'TaxaCentro'...")
    insert_into_TaxaCentro(session)

    # Insert data into 'Taxaestudo'
    print("Inserting data into 'TaxaEstudo'...")
    insert_into_TaxaEstudo(session)

    # Get list of input files
    filenames: list[str] = list_input_files()

    # Get first year of data from filenames
    years: set[int] = set(get_year_from_filename(name) for name in filenames)
    first_year: int = min(years)
    last_year: int = max(years)

    # Insert data into 'Anoacademico'
    print("Inserting data into 'Anoacademico'...")
    insert_into_Anoacademico(session, first_year, last_year)

    # Group files by content type (study_data, centre_data, subject_results)
    groups = group_files_by_type(filenames)

    # Insert data into 'Asignatura' and 'Cursase'
    print("Inserting data into 'Asignatura', 'Oferta' and 'Cursase'...")
    process_results_data(session, groups['subject_results'])

    session.commit()
    session.close()
