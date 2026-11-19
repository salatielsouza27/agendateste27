import streamlit as st
import pandas as pd

from datetime import datetime

from database.connection import SessionLocal
from database.models import (
    Cliente,
    Profissional,
    Servico,
    Agendamento
)

st.set_page_config(
    page_title="Agenda",
    layout="wide"
)

db = SessionLocal()

st.title("Agenda Inteligente")

clientes = db.query(
    Cliente
).order_by(
    Cliente.nome
).all()

profissionais = db.query(
    Profissional
).filter(
    Profissional.ativo == True
).all()

servicos = db.query(
    Servico
).filter(
    Servico.ativo == True
).all()

if not clientes:
    st.warning("Cadastre clientes primeiro")
    st.stop()

if not profissionais:
    st.warning("Cadastre profissionais primeiro")
    st.stop()

if not servicos:
    st.warning("Cadastre serviços primeiro")
    st.stop()

with st.form("novo_agendamento"):

    cliente = st.selectbox(
        "Cliente",
        clientes,
        format_func=lambda x: x.nome
    )

    profissional = st.selectbox(
        "Profissional",
        profissionais,
        format_func=lambda x: x.nome
    )

    servico = st.selectbox(
        "Serviço",
        servicos,
        format_func=lambda x: x.nome
    )

    data = st.date_input(
        "Data"
    )

    hora = st.selectbox(
        "Hora",
        [
            "08:00",
            "09:00",
            "10:00",
            "11:00",
            "12:00",
            "13:00",
            "14:00",
            "15:00",
            "16:00",
            "17:00",
            "18:00"
        ]
    )

    salvar = st.form_submit_button(
        "Agendar"
    )

    if salvar:

        conflito = db.query(
            Agendamento
        ).filter(
            Agendamento.profissional_id
            == profissional.id,
            Agendamento.data == data,
            Agendamento.hora
            == datetime.strptime(
                hora,
                "%H:%M"
            ).time()
        ).first()

        if conflito:

            st.error(
                "Horário já ocupado"
            )

        else:

            novo_agendamento = Agendamento(
                cliente_id=cliente.id,
                profissional_id=profissional.id,
                servico_id=servico.id,
                data=data,
                hora=datetime.strptime(
                    hora,
                    "%H:%M"
                ).time(),
                status="Agendado"
            )

            db.add(
                novo_agendamento
            )

            db.commit()

            st.success(
                "Agendamento realizado"
            )

            st.rerun()

st.divider()

st.subheader(
    "Agendamentos do Dia"
)

agendamentos = db.query(
    Agendamento
).order_by(
    Agendamento.data,
    Agendamento.hora
).all()

dados = []

for a in agendamentos:

    cliente = db.query(
        Cliente
    ).get(
        a.cliente_id
    )

    profissional = db.query(
        Profissional
    ).get(
        a.profissional_id
    )

    servico = db.query(
        Servico
    ).get(
        a.servico_id
    )

    dados.append({

        "Cliente":
        cliente.nome,

        "Profissional":
        profissional.nome,

        "Serviço":
        servico.nome,

        "Data":
        a.data,

        "Hora":
        a.hora,

        "Status":
        a.status

    })

if dados:

    st.dataframe(
        pd.DataFrame(
            dados
        ),
        use_container_width=True
    )

else:

    st.info(
        "Nenhum agendamento"
    )

db.close()
