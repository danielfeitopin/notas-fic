from .model import Taxaestudo, Taxacentro, Resultadoestudo, Resultadocentro, RATE_DICT, RATE_TYPES

def process_rates_and_results(YEAR: str, data: dict[str, dict[str, str]], session, rate_type, carreira=None):
    for rate_key, rate_value in data['course_data'][rate_type].items():
        if not rate_key:
            print(f"Unknown rate code: {rate_key}, skipping...")
            continue
        
        # Clean data
        rate_value = float(rate_value.replace('.', '').replace(',', '.'))
        
        # Obtain data
        category, name_info = RATE_DICT[rate_key]

        # Extract rate_name (handle both tuple and string formats)
        if isinstance(name_info, tuple):
            rate_name, _ = name_info
        else:
            rate_name = name_info

        # Determinate classes and filters based on rate type
        if rate_type == RATE_TYPES[0]:  # "Estudo"
            if not carreira:
                raise ValueError("You must provide 'carreira' for 'Estudo' rates.")
            rate = Taxaestudo
            result = Resultadoestudo
        elif rate_type == RATE_TYPES[1]:  # "Centro"
            rate = Taxacentro
            result = Resultadocentro
        else:
            raise ValueError(f"Invalid rate type: {rate_type}. Expected one of {RATE_TYPES}.")

        # Create rate if it doesn't exist
        if rate_type == RATE_TYPES[0]:
            existing_rate = session.query(rate).filter(
                rate.codigo == rate_key,
                rate.codigo_carreira == carreira
            ).first()
            if not existing_rate:
                new_rate = rate(codigo=rate_key, codigo_carreira=carreira, nome=rate_name, categoria=category)
                print(f"Creating {rate.__name__}: {new_rate}")
                session.add(new_rate)
            else:
                print(f"{rate.__name__} already exists: {existing_rate}")

            existing_result = session.query(result).filter(
                result.codigo_anoacademico == YEAR,
                result.codigo_taxa == rate_key,
                result.codigo_carreira == carreira
            ).first()
            if not existing_result:
                new_result = result(codigo_anoacademico=YEAR, codigo_taxa=rate_key, codigo_carreira=carreira, valor=rate_value)
                print(f"Creating {result.__name__}: {new_result}")
                session.add(new_result)
        else:
            existing_rate = session.query(rate).filter(
                rate.codigo == rate_key
            ).first()
            if not existing_rate:
                new_rate = rate(codigo=rate_key, nome=rate_name, categoria=category)
                print(f"Creating {rate.__name__}: {new_rate}")
                session.add(new_rate)
            else:
                print(f"{rate.__name__} already exists: {existing_rate}")

            existing_result = session.query(result).filter(
                result.codigo_anoacademico == YEAR,
                result.codigo_taxa == rate_key
            ).first()
            if not existing_result:
                new_result = result(codigo_anoacademico=YEAR, codigo_taxa=rate_key, valor=rate_value)
                print(f"Creating {result.__name__}: {new_result}")
                session.add(new_result)

    session.commit()