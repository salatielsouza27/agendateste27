from sqlalchemy import (
    Column,
    Integer,
    String,
    Float,
    Date,
    Time,
    DateTime,
    ForeignKey,
    Boolean
)

from sqlalchemy.orm import relationship
from datetime import datetime

from database.connection import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    nome = Column(String(150), nullable=False)

    email = Column(
        String(150),
        unique=True,
        nullable=False
    )

    senha = Column(String(255), nullable=False)

    perfil = Column(String(50), nullable=False)

    ativo = Column(
        Boolean,
        default=True
    )

    criado_em = Column(
        DateTime,
        default=datetime.utcnow
    )


class Cliente(Base):
    __tablename__ = "clientes"

    id = Column(Integer, primary_key=True)

    nome = Column(
        String(150),
        nullable=False
    )

    telefone = Column(String(30))

    email = Column(String(150))

    observacoes = Column(String(500))

    criado_em = Column(
        DateTime,
        default=datetime.utcnow
    )

    agendamentos = relationship(
        "Agendamento",
        back_populates="cliente"
    )


class Profissional(Base):
    __tablename__ = "profissionais"

    id = Column(Integer, primary_key=True)

    nome = Column(
        String(150),
        nullable=False
    )

    telefone = Column(String(30))

    especialidade = Column(
        String(100)
    )

    ativo = Column(
        Boolean,
        default=True
    )

    criado_em = Column(
        DateTime,
        default=datetime.utcnow
    )

    agendamentos = relationship(
        "Agendamento",
        back_populates="profissional"
    )


class Servico(Base):
    __tablename__ = "servicos"

    id = Column(Integer, primary_key=True)

    nome = Column(
        String(150),
        nullable=False
    )

    descricao = Column(String(500))

    duracao = Column(Integer)

    valor = Column(Float)

    ativo = Column(
        Boolean,
        default=True
    )

    agendamentos = relationship(
        "Agendamento",
        back_populates="servico"
    )


class Agendamento(Base):
    __tablename__ = "agendamentos"

    id = Column(Integer, primary_key=True)

    cliente_id = Column(
        Integer,
        ForeignKey("clientes.id")
    )

    profissional_id = Column(
        Integer,
        ForeignKey("profissionais.id")
    )

    servico_id = Column(
        Integer,
        ForeignKey("servicos.id")
    )

    data = Column(Date)

    hora = Column(Time)

    status = Column(
        String(50),
        default="Agendado"
    )

    observacao = Column(String(500))

    criado_em = Column(
        DateTime,
        default=datetime.utcnow
    )

    cliente = relationship(
        "Cliente",
        back_populates="agendamentos"
    )

    profissional = relationship(
        "Profissional",
        back_populates="agendamentos"
    )

    servico = relationship(
        "Servico",
        back_populates="agendamentos"
    )
