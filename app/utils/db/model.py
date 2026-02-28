from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, Float
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

Base = declarative_base()
engine = None
Session = None

RATE_TYPES = ["Estudo", "Centro"]

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

RATE_DICT = {
    "STUDY_0": (RATE_TYPES[0], RATE_CATEGORIES[0], RATE_NAMES[0]),
    "STUDY_1": (RATE_TYPES[0], RATE_CATEGORIES[0], RATE_NAMES[1]),
    "STUDY_2": (RATE_TYPES[0], RATE_CATEGORIES[0], RATE_NAMES[2]),
    "STUDY_3": (RATE_TYPES[0], RATE_CATEGORIES[1], RATE_NAMES[3]),
    "STUDY_4": (RATE_TYPES[0], RATE_CATEGORIES[1], RATE_NAMES[4]),
    "STUDY_5": (RATE_TYPES[0], RATE_CATEGORIES[1], RATE_NAMES[5]),
    "STUDY_6": (RATE_TYPES[0], RATE_CATEGORIES[1], RATE_NAMES[6]),
    "STUDY_7": (RATE_TYPES[0], RATE_CATEGORIES[1], RATE_NAMES[7]),
    "STUDY_8": (RATE_TYPES[0], RATE_CATEGORIES[1], RATE_NAMES[8]),
    "STUDY_9": (RATE_TYPES[0], RATE_CATEGORIES[2], RATE_NAMES[9]),
    "STUDY_10": (RATE_TYPES[0], RATE_CATEGORIES[2], RATE_NAMES[10]),
    "STUDY_11": (RATE_TYPES[0], RATE_CATEGORIES[2], RATE_NAMES[11]),
    "STUDY_12": (RATE_TYPES[0], RATE_CATEGORIES[2], RATE_NAMES[12]),
    "STUDY_13": (RATE_TYPES[0], RATE_CATEGORIES[2], RATE_NAMES[13]),
    "STUDY_14": (RATE_TYPES[0], RATE_CATEGORIES[2], RATE_NAMES[14]),
    "CENTRE_0": (RATE_TYPES[1], RATE_CATEGORIES[0], RATE_NAMES[0]),
    "CENTRE_1": (RATE_TYPES[1], RATE_CATEGORIES[0], RATE_NAMES[1]),
    "CENTRE_2": (RATE_TYPES[1], RATE_CATEGORIES[0], RATE_NAMES[2]),
    "CENTRE_3": (RATE_TYPES[1], RATE_CATEGORIES[1], RATE_NAMES[3]),
    "CENTRE_4": (RATE_TYPES[1], RATE_CATEGORIES[1], RATE_NAMES[4]),
    "CENTRE_5": (RATE_TYPES[1], RATE_CATEGORIES[1], RATE_NAMES[5]),
    "CENTRE_6": (RATE_TYPES[1], RATE_CATEGORIES[1], RATE_NAMES[6]),
    "CENTRE_7": (RATE_TYPES[1], RATE_CATEGORIES[1], RATE_NAMES[7]),
    "CENTRE_8": (RATE_TYPES[1], RATE_CATEGORIES[1], RATE_NAMES[8]),
    "CENTRE_9": (RATE_TYPES[1], RATE_CATEGORIES[2], RATE_NAMES[9]),
    "CENTRE_10": (RATE_TYPES[1], RATE_CATEGORIES[2], RATE_NAMES[10]),
    "CENTRE_11": (RATE_TYPES[1], RATE_CATEGORIES[2], RATE_NAMES[11])
}


# Tables
class Carreira(Base):
    __tablename__ = "Carreira"
    Código = Column(String, primary_key=True)
    Nome = Column(String, nullable=False)
    Siglas = Column(String, nullable=False)


class Asignatura(Base):
    __tablename__ = "Asignatura"
    Código = Column(String, primary_key=True)
    Nome = Column(String, nullable=False)
    Siglas = Column(String, nullable=False)


class Anoacademico(Base):
    __tablename__ = "Anoacadémico"
    Código = Column(String, primary_key=True)
    Inicio = Column(Integer, nullable=False)
    Fin = Column(Integer, nullable=False)


class Taxa(Base):
    __tablename__ = "Taxa"
    Código = Column(String, primary_key=True)
    Tipo = Column(String, nullable=False)
    Categoría = Column(String, nullable=False)
    Nome = Column(String, nullable=False)


class Oferta(Base):
    __tablename__ = "Oferta"
    Código_Carreira = Column(String, ForeignKey("Carreira.Código"), primary_key=True)
    Código_Asignatura = Column(
        String, ForeignKey("Asignatura.Código"), primary_key=True
    )
    Curso = Column(Integer, nullable=False)


class Cursase(Base):
    __tablename__ = "Cúrsase"
    Código_Anoacadémico = Column(
        String, ForeignKey("Anoacadémico.Código"), primary_key=True
    )
    Código_Asignatura = Column(
        String, ForeignKey("Asignatura.Código"), primary_key=True
    )
    Aprobados = Column(Integer, nullable=False)
    Suspensos = Column(Integer, nullable=False)
    NP = Column(Integer, nullable=False)


class Resultado(Base):
    __tablename__ = "Resultado"
    Código_Anoacadémico = Column(
        String, ForeignKey("Anoacadémico.Código"), primary_key=True
    )
    Código_Taxa = Column(String, ForeignKey("Taxa.Código"), primary_key=True)
    Valor = Column(Float, nullable=False)


def init_database(db_path: str = "sqlite:///notasfic.db"):
    """Initializes the database connection and returns the engine."""
    global engine, Session
    engine = create_engine(db_path)
    Session = sessionmaker(bind=engine)
    return engine


def create_tables():
    """Creates the tables in the database based on the defined models."""
    if engine is None:
        raise RuntimeError("You must call init_database() before create_tables()")

    Base.metadata.create_all(engine)

    # Show created tables
    for table in Base.metadata.tables:
        print(f"Táboa creada: {table}")
