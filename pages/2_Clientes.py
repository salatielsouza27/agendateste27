import streamlit as st
import pandas as pd
import sqlite3

st.set_page_config(
    page_title="Clientes",
    layout="wide"
)

st.title("👥 Cadastro de Clientes")

conn = sqlite3.connect(
    "beautyschedule.db",
    check_same_thread=False
)

cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS clientes (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nome TEXT,
    telefone TEXT,
    email TEXT,
    observacoes TEXT
)
""")

conn.commit()

# FORMULÁRIO

with st.container():

    st.subheader("Novo Cliente")

    col1, col2 = st.columns(2)

    with col1:
        nome = st.text_input("Nome")

        telefone = st.text_input(
            "Telefone"
        )

    with col2:

        email = st.text_input(
            "E-mail"
        )

    observacoes = st.text_area(
        "Observações"
    )

    if st.button(
        "Salvar Cliente"
    ):

        cursor.execute(
            """
            INSERT INTO clientes
            (
                nome,
                telefone,
                email,
                observacoes
            )
            VALUES (?, ?, ?, ?)
            """,
            (
                nome,
                telefone,
                email,
                observacoes
            )
        )

        conn.commit()

        st.success(
            "Cliente salvo com sucesso"
        )

        st.rerun()

st.divider()

# TABELA

st.subheader(
    "Clientes Cadastrados"
)

df = pd.read_sql_query(
    """
    SELECT
    id,
    nome,
    telefone,
    email,
    observacoes
    FROM clientes
    ORDER BY id DESC
    """,
    conn
)

st.dataframe(
    df,
    use_container_width=True
)

# EXCLUSÃO

if len(df) > 0:

    st.divider()

    cliente_id = st.selectbox(
        "Excluir Cliente",
        df["id"]
    )

    if st.button(
        "Excluir"
    ):

        cursor.execute(
            """
            DELETE FROM clientes
            WHERE id = ?
            """,
            (int(cliente_id),)
        )

        conn.commit()

        st.success(
            "Cliente excluído"
        )

        st.rerun()

conn.close()
