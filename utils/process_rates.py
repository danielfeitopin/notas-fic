from .model import  Taxa, Resultado, RATE_DICT

def process_rates_and_results(YEAR: str, data: dict[str, dict[str, str]], session, rate_type):
    for rate_key, rate_value in data['course_data'][rate_type].items():
        if not rate_key:
            print(f"Unknown rate code: {rate_key}, skipping...")
            continue
        
        rate_value = rate_value.replace('.', '')
        rate_value = rate_value.replace(',', '.')
        
        existing_rate = session.query(Taxa).filter_by(Código=rate_key).first()
        if not existing_rate:
            new_rate = Taxa(Código=rate_key, Tipo=RATE_DICT[rate_key][0], Categoría=RATE_DICT[rate_key][1], Nome=RATE_DICT[rate_key][2])
            print(f"Creating Rate: {new_rate.Código} - {new_rate.Nome}")
            session.add(new_rate)
        if existing_rate:
            print(f"Rate already exists: {existing_rate.Código} - {existing_rate.Nome}")
            
        existing_result = session.query(Resultado).filter_by(
            Código_Anoacadémico=YEAR,
            Código_Taxa=rate_key
        ).first()
        
        if not existing_result:
            new_result = Resultado(
                Valor=rate_value,
                Código_Anoacadémico=YEAR,
                Código_Taxa=rate_key
            )
            print(f"Creating Resultado: {new_result.Código_Anoacadémico} - {new_result.Código_Taxa} - {new_result.Valor}")
            session.add(new_result)