import streamlit as st
import pandas as pd
import sqlite3

st.set_page_config(
    page_title="Agenda",
    layout="wide"
)

st.title("Agenda Inteligente")

conn = sqlite3.connect(
    "beautyschedule.db",
    check_same_thread=False
)

# Cria tabela se não existir
conn.execute("""
CREATE TABLE IF NOT EXISTS agendamentos (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    cliente TEXT,
    profissional TEXT,
    servico TEXT,
    data TEXT,
    hora TEXT,
    status TEXT
)
""")

st.subheader("Novo Agendamento")

with st.form("agenda"):

    cliente = st.text_input("Cliente")

    profissional = st.text_input("Profissional")

    servico = st.text_input("Serviço")

    data = st.date_input("Data")

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

        conflito = conn.execute(
            """
            SELECT *
            FROM agendamentos
            WHERE profissional=?
            AND data=?
            AND hora=?
            """,
            (
                profissional,
                str(data),
                hora
            )
        ).fetchone()

        if conflito:

            st.error(
                "Horário já ocupado para este profissional."
            )

        else:

            conn.execute(
                """
                INSERT INTO agendamentos
                (
                    cliente,
                    profissional,
                    servico,
                    data,
                    hora,
                    status
                )
                VALUES
                (?, ?, ?, ?, ?, ?)
                """,
                (
                    cliente,
                    profissional,
                    servico,
                    str(data),
                    hora,
                    "Agendado"
                )
            )

            conn.commit()

            st.success(
                "Agendamento realizado com sucesso"
            )

st.divider()

st.subheader("Agenda")

df = pd.read_sql_query(
    """
    SELECT *
    FROM agendamentos
    ORDER BY data,hora
    """,
    conn
)

if len(df) > 0:

    st.dataframe(
        df,
        use_container_width=True
    )

else:

    st.info(
        "Nenhum agendamento cadastrado."
    )

conn.close()
