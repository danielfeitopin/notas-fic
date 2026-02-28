from . import model
from .model import Asignatura, Cursase, Anoacademico, Carreira, Oferta, init_database, create_tables
from .process_rates import process_rates_and_results

def insert_data_into_db(YEAR: str, STUDY_CODE: str, data: dict[str, dict[str, str]]):
    # Initialize database and create tables
    init_database('sqlite:///notasfic.db')
    create_tables()
    session = model.Session()
    print(f"Created session: {session}")

    # Register the academic year (Anoacademico)
    year_db = session.query(Anoacademico).filter_by(Código=YEAR).first()
    if not year_db:
        year_db = Anoacademico(Código=YEAR, Inicio=int(YEAR), Fin=int(YEAR)+1)
        session.add(year_db)

    # Register the degree (Carreira)
    degree_db = session.query(Carreira).filter_by(Código=STUDY_CODE).first()
    if not degree_db:
        degree_db = Carreira(Código=STUDY_CODE, Nome="Grao en Ciencia e Enxeñaría de Datos", Siglas="GCED")
        session.add(degree_db)

    # Formatting and inserting subject data
    asig_counter = 1  
    print(f"Processing {len(data['subject_results'])} courses...")
    for course_num, subjects_list in data['subject_results'].items():
        print(f"Course {course_num}: {len(subjects_list)} subjects")
        for item in subjects_list:
            subject_name = item['name']
            passed, failed, np = map(int, item['metrics'])
            
            subject_db = session.query(Asignatura).filter_by(Nome=subject_name).first()
            if not subject_db:
                subject_code = str(asig_counter)
                subject_db = Asignatura(Código=subject_code, Nome=subject_name, Siglas=subject_name[:5])
                session.add(subject_db)
                session.flush()
                print(f"Created subject: {subject_name} (Code: {subject_code})")
                asig_counter += 1
            else:
                print(f"Subject already exists: {subject_name}")

            # Register the course offering (Oferta)
            existing_offer = session.query(Oferta).filter_by(
                Curso=course_num, 
                Código_Carreira=STUDY_CODE, 
                Código_Asignatura=subject_db.Código
            ).first()
            
            if not existing_offer:
                new_offer = Oferta(Curso=course_num, Código_Carreira=STUDY_CODE, Código_Asignatura=subject_db.Código)
                session.add(new_offer)

            # Register the results (Cursase)
            existing_taken = session.query(Cursase).filter_by(
                Código_Anoacadémico=YEAR,
                Código_Asignatura=subject_db.Código
            ).first()
            if not existing_taken:
                new_register = Cursase(
                    Código_Anoacadémico=YEAR,
                    Código_Asignatura=subject_db.Código,
                    Aprobados=passed,
                    Suspensos=failed,
                    NP=np
                )
                session.add(new_register)
                
    # Register the rates (Taxa) and results (Resultado)
    print("Processing rates and results...")
    process_rates_and_results(YEAR, data, session, 'study_data')
    process_rates_and_results(YEAR, data, session, 'centre_data')
    print("Finished processing rates and results.")

    # Confirm changes
    try:
        session.commit()
        print(f"Data successfully saved to notasfic.db")
    except Exception as e:
        print(f"Error saving data: {e}")
        import traceback
        traceback.print_exc()
        session.rollback()
    finally:
        session.close()