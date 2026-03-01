from sqlalchemy import Column, Integer, String, ForeignKey, Float
from sqlalchemy.ext.declarative import declarative_base


Base = declarative_base()


class Carreira(Base):
    __tablename__ = "Carreira"
    codigo = Column("Código", String, primary_key=True)
    nome = Column("Nome", String, nullable=False)
    siglas = Column("Siglas", String, nullable=False)


class Asignatura(Base):
    __tablename__ = "Asignatura"
    codigo = Column("Código", String, primary_key=True)
    codigo_carreira = Column("Código_Carreira", String, ForeignKey(
        "Carreira.Código"), nullable=False)
    nome = Column("Nome", String, nullable=False)
    curso = Column("Curso", Integer, nullable=False)


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
    codigo_carreira = Column("Código_Carreira", String, ForeignKey(
        "Carreira.Código"), primary_key=True)


class Taxacentro(Base):
    __tablename__ = "Taxacentro"
    codigo = Column("Código", String, primary_key=True)
    categoria = Column("Categoría", String, nullable=False)
    nome = Column("Nome", String, nullable=False)


# class Oferta(Base):
#     __tablename__ = "Oferta"
#     codigo_carreira = Column("Código_Carreira", String, ForeignKey(
#         "Carreira.Código"), primary_key=True)
#     codigo_asignatura = Column(
#         "Código_Asignatura", String, ForeignKey("Asignatura.Código"), primary_key=True
#     )
#     curso = Column(Integer, nullable=False)


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
    codigo_taxa = Column("Código_Taxa", String, ForeignKey(
        "Taxaestudo.Código"), primary_key=True)
    codigo_carreira = Column("Código_Carreira", String, ForeignKey(
        "Carreira.Código"), primary_key=True)
    valor = Column("Valor", Float, nullable=False)


class Resultadocentro(Base):
    __tablename__ = "Resultadocentro"
    codigo_anoacademico = Column(
        "Código_Anoacadémico", String, ForeignKey("Anoacadémico.Código"), primary_key=True
    )
    codigo_taxa = Column("Código_Taxa", String, ForeignKey(
        "Taxacentro.Código"), primary_key=True)
    valor = Column("Valor", Float, nullable=False)
