# SPDX-FileCopyrightText: 2026 Daniel Feito-Pin <danielfeitopin+github@protonmail.com>
#
# SPDX-License-Identifier: GPL-3.0-or-later

from flask import render_template, jsonify, Flask
from sqlalchemy import text
from app.utils.db import SESSION

def create_routes(app: Flask):
    @app.route('/')
    def index():
        """Render main page"""
        return render_template('index.html')

    @app.route('/carrera/<siglas>')
    def carrera_page(siglas):
        """Page dedicated to a specific career."""
        return render_template('index.html', selected_carrera=siglas)


    @app.route('/asignatura/<codigo>')
    def asignatura_page(codigo):
        """Page dedicated to a specific subject."""
        return render_template('subject.html', codigo_asignatura=codigo)

    @app.route('/carrera/<siglas>/ano/<ano>')
    def carrera_ano_page(siglas, ano):
        """Page dedicated to an academic year within a career."""
        return render_template('year.html', carrera=siglas, ano=ano)

    # ============== API ENDPOINTS ==============

    # A) 
    @app.route('/api/resultados/top-suspensos-por-ano')
    def get_top_failed_per_year():
        """Obtains the subject with the most fails for each academic year"""
        db_session = SESSION()

        query = text("""
            SELECT *
            FROM (
                SELECT 
                    car.Siglas as carreira,
                    aa.Inicio || '-' || aa.Fin as ano,
                    a.Código,
                    a.Nome,
                    c.Aprobados,
                    c.Suspensos,
                    c.NP,
                    ROW_NUMBER() OVER (
                        PARTITION BY car.Código, aa.Código
                        ORDER BY c.Suspensos DESC
                    ) as rn
                FROM "Cúrsase" c
                JOIN Asignatura a ON c.Código_Asignatura = a.Código
                JOIN Carreira car ON a.Código_Carreira = car.Código
                JOIN "Anoacadémico" aa ON c.Código_Anoacadémico = aa.Código
            ) sub
            WHERE rn = 1
            ORDER BY carreira, ano
        """)

        # result = db_session.execute(query)
        with SESSION() as db_session:
            result = db_session.execute(query)

        data = [{
            "carreira": row[0],
            "ano": row[1],
            "codigo_asignatura": row[2],
            "asignatura": row[3],
            "aprobados": row[4],
            "suspensos": row[5],
            "np": row[6]
        } for row in result]

        return jsonify(data)

    # B)
    @app.route('/api/resultados/evolucion/<codigo_asignatura>')
    def get_subject_evolution(codigo_asignatura):
        """Obtains the evolution of results for a specific subject across academic years"""
        db_session = SESSION()

        query = text("""
            SELECT 
                aa.Inicio || '-' || aa.Fin as ano,
                c.Aprobados,
                c.Suspensos,
                c.NP
            FROM "Cúrsase" c
            JOIN "Anoacadémico" aa ON c.Código_Anoacadémico = aa.Código
            WHERE c.Código_Asignatura = :codigo
            ORDER BY aa.Inicio
        """)

        with SESSION() as db_session:
            result = db_session.execute(query, {"codigo": codigo_asignatura})
        

        data = [{
            "ano": row[0],
            "aprobados": row[1],
            "suspensos": row[2],
            "np": row[3]
        } for row in result]

        return jsonify(data)


    # C)
    @app.route('/api/resultados/top-np-por-carreira')
    def get_top_np_per_career():
        """Top 3 subjects with the highest NP percentage for each career and academic year"""
        db_session = SESSION()

        query = text("""
            WITH ranked AS (
                SELECT
                    car.Siglas as carreira,
                    aa.Inicio || '-' || aa.Fin as ano,
                    a.Código,
                    a.Nome,
                    ROUND(
                        (CAST(SUM(c.NP) AS REAL) / 
                         NULLIF(SUM(c.Aprobados + c.Suspensos + c.NP), 0)) * 100,
                        2
                    ) as porcentaxe_np,
                    ROW_NUMBER() OVER (
                        PARTITION BY car.Código, aa.Código
                        ORDER BY 
                            (CAST(SUM(c.NP) AS REAL) /
                             NULLIF(SUM(c.Aprobados + c.Suspensos + c.NP), 0)) DESC
                    ) as rn
                FROM "Cúrsase" c
                JOIN Asignatura a ON c.Código_Asignatura = a.Código
                JOIN Carreira car ON a.Código_Carreira = car.Código
                JOIN "Anoacadémico" aa ON c.Código_Anoacadémico = aa.Código
                GROUP BY car.Código, car.Siglas, aa.Código, aa.Inicio, aa.Fin, a.Código, a.Nome
            )
            SELECT carreira, ano, 1, Código, Nome, porcentaxe_np
            FROM ranked
            WHERE rn <= 3
            ORDER BY carreira, ano, porcentaxe_np DESC
        """)
        with SESSION() as db_session:
            result = db_session.execute(query)

        data = [{
            "carreira": row[0],
            "ano": row[1],
            "curso": row[2],
            "codigo_asignatura": row[3],
            "asignatura": row[4],
            "porcentaxe_np": float(row[5]) if row[5] else 0
        } for row in result]

        return jsonify(data)


    # D)
    @app.route('/api/resultados/evolucion-carreira/<codigo_carreira>')
    def get_career_evolution(codigo_carreira):
        """Temporary evolution of passed, failed and NP for a career"""
        db_session = SESSION()

        if codigo_carreira.lower() != codigo_carreira or len(codigo_carreira) > 5:
            query_filter = "car.Siglas = :carreira"
        else:
            query_filter = "car.Código = :carreira"
        
        query = text(f"""
            SELECT
                aa.Inicio || '-' || aa.Fin as ano,
                SUM(c.Aprobados) as aprobados,
                SUM(c.Suspensos) as suspensos,
                SUM(c.NP) as np
            FROM "Cúrsase" c
            JOIN Asignatura a ON c.Código_Asignatura = a.Código
            JOIN Carreira car ON a.Código_Carreira = car.Código
            JOIN "Anoacadémico" aa ON c.Código_Anoacadémico = aa.Código
            WHERE {query_filter}
            GROUP BY aa.Inicio, aa.Fin
            ORDER BY aa.Inicio
        """)

        with SESSION() as db_session:
            result = db_session.execute(query, {"carreira": codigo_carreira})

        data = [{
            "ano": row[0],
            "aprobados": row[1],
            "suspensos": row[2],
            "np": row[3]
        } for row in result]

        return jsonify(data)

    #E
    @app.route('/api/resultados/porcentaxe-sexo/<codigo_ano>')
    def get_gender_percentage(codigo_ano):
        """Obtains the percentage of male and female students for each career and academic year.
        Returns ALL careers, including those without gender data."""
        db_session = SESSION()
        
        ano_db = codigo_ano.replace('-', '_')
        
        # First get all careers
        all_carreiras_query = text("SELECT Código, Siglas FROM Carreira ORDER BY Siglas")
        all_carreiras = db_session.execute(all_carreiras_query)
        all_carreiras_dict = {row[1]: row[0] for row in all_carreiras}
       
        # Then get the data for this year
        query = text("""
            SELECT
                c.Siglas as carreira,
                t.Nome as xenero,
                r.Valor as valor
            FROM Resultadoestudo r
            JOIN Taxaestudo t
                ON r.Código_Taxa = t.Código
               AND r.Código_Carreira = t.Código_Carreira
            JOIN Carreira c
                ON r.Código_Carreira = c.Código
            WHERE r.Código_Anoacadémico = :ano
              AND t.Nome IN ('Homes', 'Mulleres')
            ORDER BY c.Siglas""")
       
        result = db_session.execute(query, {"ano": ano_db})
       
        data = {}
     
        for row in result:
            carreira = row.carreira
            if carreira not in data:
                data[carreira] = {"Homes": 0, "Mulleres": 0}
     
            data[carreira][row.xenero] = row.valor
     
        response = []
     
        # Iterate over ALL careers, not just those with data
        for carreira in sorted(all_carreiras_dict.keys()):
            if carreira in data:
                valores = data[carreira]
            else:
                valores = {"Homes": 0, "Mulleres": 0}
     
            total = valores["Homes"] + valores["Mulleres"]
     
            if total == 0:
                porcentaje_homes = 0
                porcentaje_mulleres = 0
            else:
                porcentaje_homes = round((valores["Homes"] / total) * 100, 2)
                porcentaje_mulleres = round((valores["Mulleres"] / total) * 100, 2)
     
            response.append({
                "carreira": carreira,
                "homes": valores["Homes"],
                "mulleres": valores["Mulleres"],
                "porcentaje_homes": porcentaje_homes,
                "porcentaje_mulleres": porcentaje_mulleres
            })
     
        return jsonify(response)

    # Additional API endpoints
    @app.route('/api/carreiras')
    def get_carreiras():
        """Get all careers"""
        db_session = SESSION()

        result = db_session.execute(text("SELECT DISTINCT Código, Nome, Siglas FROM Carreira ORDER BY Siglas"))
        carreiras = [{"codigo": row[0], "nome": row[1], "siglas": row[2]} for row in result]
        return jsonify(carreiras)

    @app.route('/api/asignaturas/<carrera>')
    def get_asignaturas(carrera):
        """Get subjects for a specific career."""
        db_session = SESSION()

        query = text("""
            SELECT a.Código, a.Nome 
            FROM Asignatura a
            JOIN Carreira car ON a.Código_Carreira = car.Código
            WHERE car.Siglas = :siglas
        """)
        result = db_session.execute(query, {"siglas": carrera})
        asignaturas = [{"codigo": row[0], "nome": row[1]} for row in result]
        return jsonify(asignaturas)

    @app.route('/api/anos')
    def get_anos():
        """Returns the list of academic years."""
        db_session = SESSION()

        result = db_session.execute(text(
            "SELECT Inicio || '-' || Fin as ano FROM \"Anoacadémico\" ORDER BY Inicio"
        ))
        anos = [{"ano": row[0]} for row in result]
        return jsonify(anos)

    @app.route('/api/resultados/comparacion-carreras')
    def get_comparacion_carreras():
        """Get comparison of results between careers"""
        db_session = SESSION()

        query = text("""
            SELECT 
                car.Siglas,
                SUM(c.Aprobados) as total_aprobados,
                SUM(c.Suspensos) as total_suspensos,
                COUNT(DISTINCT c.Código_Asignatura) as num_asignaturas
            FROM "Cúrsase" c
            JOIN Asignatura a ON c.Código_Asignatura = a.Código
            JOIN Carreira car ON a.Código_Carreira = car.Código
            GROUP BY car.Código, car.Siglas
        """)
        result = db_session.execute(query)
        datos = [{
            "carrera": row[0],
            "aprobados": row[1],
            "suspensos": row[2],
            "asignaturas": row[3]
        } for row in result]
        return jsonify(datos)

    @app.route('/api/resultados/suspensos/<carrera>')
    def get_suspensos_por_carrera(carrera):
        """Get subjects with most fails for a specific career"""
        db_session = SESSION()

        query = text("""
            SELECT 
                a.Nome,
                SUM(c.Suspensos) as total_suspensos,
                SUM(c.Aprobados) as total_aprobados,
                SUM(c.NP) as total_np,
                SUM(c.Aprobados + c.Suspensos + c.NP) as total_alumnos
            FROM "Cúrsase" c
            JOIN Asignatura a ON c.Código_Asignatura = a.Código
            JOIN Carreira car ON a.Código_Carreira = car.Código
            WHERE car.Siglas = :carrera OR car.Código = :carrera
            GROUP BY a.Código, a.Nome
            ORDER BY total_suspensos DESC
            LIMIT 10
        """)
        result = db_session.execute(query, {"carrera": carrera})
        datos = [{
            "asignatura": row[0],
            "suspensos": row[1],
            "aprobados": row[2],
            "np": row[3],
            "total": row[4]
        } for row in result]
        return jsonify(datos)
