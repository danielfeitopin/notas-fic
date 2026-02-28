from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, Float
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

Base = declarative_base()
engine = None
Session = None

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

RATE_DICT = {
    "STUDY_0": (RATE_CATEGORIES[0], (RATE_NAMES[0], None)),
    "STUDY_1": (RATE_CATEGORIES[0], (RATE_NAMES[1], None)),
    "STUDY_2": (RATE_CATEGORIES[0], (RATE_NAMES[2], None)),
    "STUDY_3": (RATE_CATEGORIES[1], (RATE_NAMES[3], None)),
    "STUDY_4": (RATE_CATEGORIES[1], (RATE_NAMES[4], None)),
    "STUDY_5": (RATE_CATEGORIES[1], (RATE_NAMES[5], None)),
    "STUDY_6": (RATE_CATEGORIES[1], (RATE_NAMES[6], None)),
    "STUDY_7": (RATE_CATEGORIES[1], (RATE_NAMES[7], None)),
    "STUDY_8": (RATE_CATEGORIES[1], (RATE_NAMES[8], None)),
    "STUDY_9": (RATE_CATEGORIES[2], (RATE_NAMES[9], None)),
    "STUDY_10": (RATE_CATEGORIES[2], (RATE_NAMES[10], None)),
    "STUDY_11": (RATE_CATEGORIES[2], (RATE_NAMES[11], None)),
    "STUDY_12": (RATE_CATEGORIES[2], (RATE_NAMES[12], None)),
    "STUDY_13": (RATE_CATEGORIES[2], (RATE_NAMES[13], None)),
    "STUDY_14": (RATE_CATEGORIES[2], (RATE_NAMES[14], None)),
    "CENTRE_0": (RATE_CATEGORIES[0], RATE_NAMES[0]),
    "CENTRE_1": (RATE_CATEGORIES[0], RATE_NAMES[1]),
    "CENTRE_2": (RATE_CATEGORIES[0], RATE_NAMES[2]),
    "CENTRE_3": (RATE_CATEGORIES[1], RATE_NAMES[3]),
    "CENTRE_4": (RATE_CATEGORIES[1], RATE_NAMES[4]),
    "CENTRE_5": (RATE_CATEGORIES[1], RATE_NAMES[5]),
    "CENTRE_6": (RATE_CATEGORIES[1], RATE_NAMES[6]),
    "CENTRE_7": (RATE_CATEGORIES[1], RATE_NAMES[7]),
    "CENTRE_8": (RATE_CATEGORIES[1], RATE_NAMES[8]),
    "CENTRE_9": (RATE_CATEGORIES[2], RATE_NAMES[9]),
    "CENTRE_10": (RATE_CATEGORIES[2], RATE_NAMES[10]),
    "CENTRE_11": (RATE_CATEGORIES[2], RATE_NAMES[11])
}


# Tables
class Carreira(Base):
    __tablename__ = "Carreira"
    codigo = Column("Código", String, primary_key=True)
    nome = Column("Nome", String, nullable=False)
    siglas = Column("Siglas", String, nullable=False)


class Asignatura(Base):
    __tablename__ = "Asignatura"
    codigo = Column("Código", String, primary_key=True)
    nome = Column("Nome", String, nullable=False)
    siglas = Column("Siglas", String, nullable=False)


class Anoacademico(Base):
    __tablename__ = "Anoacadémico"
    codigo = Column("Código", String, primary_key=True)
    inicio = Column("Inicio", Integer, nullable=False)
    fin = Column("Fin", Integer, nullable=False)


class Taxaestudo(Base):
    __tablename__ = "Taxaestudo"
    codigo = Column("Código", String, primary_key=True)
    categoria = Column("Categoría", String, nullable=False)
    nome = Column("Nome", String, nullable=False)
    codigo_carreira = Column("Código_Carreira", String, ForeignKey("Carreira.Código"), primary_key=True)
    
class Taxacentro(Base):
    __tablename__ = "Taxacentro"
    codigo = Column("Código", String, primary_key=True)
    categoria = Column("Categoría", String, nullable=False)
    nome = Column("Nome", String, nullable=False)


class Oferta(Base):
    __tablename__ = "Oferta"
    codigo_carreira = Column("Código_Carreira", String, ForeignKey("Carreira.Código"), primary_key=True)
    codigo_asignatura = Column(
        "Código_Asignatura", String, ForeignKey("Asignatura.Código"), primary_key=True
    )
    curso = Column(Integer, nullable=False)


class Cursase(Base):
    __tablename__ = "Cúrsase"
    codigo_anoacademico = Column(
        "Código_Anoacadémico", String, ForeignKey("Anoacadémico.Código"), primary_key=True
    )
    codigo_asignatura = Column(
        "Código_Asignatura", String, ForeignKey("Asignatura.Código"), primary_key=True
    )
    aprobados = Column("Aprobados", Integer, nullable=False)
    suspensos = Column("Suspensos", Integer, nullable=False)
    np = Column("NP", Integer, nullable=False)


class Resultadoestudo(Base):
    __tablename__ = "Resultadoestudo"
    codigo_anoacademico = Column(
        "Código_Anoacadémico", String, ForeignKey("Anoacadémico.Código"), primary_key=True
    )
    codigo_taxa = Column("Código_Taxa", String, ForeignKey("Taxaestudo.Código"), primary_key=True)
    codigo_carreira = Column("Código_Carreira", String, ForeignKey("Carreira.Código"), primary_key=True)
    valor = Column("Valor", Float, nullable=False)
    
class Resultadocentro(Base):
    __tablename__ = "Resultadocentro"
    codigo_anoacademico = Column(
        "Código_Anoacadémico", String, ForeignKey("Anoacadémico.Código"), primary_key=True
    )
    codigo_taxa = Column("Código_Taxa", String, ForeignKey("Taxacentro.Código"), primary_key=True)
    valor = Column("Valor", Float, nullable=False)


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
