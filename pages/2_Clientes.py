import streamlit as st
import sqlite3
import pandas as pd

st.set_page_config(
    page_title="Clientes",
    layout="wide"
)

st.title("Clientes")

conn = sqlite3.connect(
    "beautyschedule.db",
    check_same_thread=False
)

cursor = conn.cursor()

# recria tabela corretamente

cursor.execute("""
CREATE TABLE IF NOT EXISTS clientes (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nome TEXT
)
""")

conn.commit()

# =====================
# CADASTRO
# =====================

nome = st.text_input(
    "Nome do Cliente"
)

if st.button("Salvar"):

    if nome:

        cursor.execute(
            """
            INSERT INTO clientes(nome)
            VALUES(?)
            """,
            (nome,)
        )

        conn.commit()

        st.success(
            "Cliente cadastrado"
        )

# =====================
# LISTAGEM
# =====================

st.subheader(
    "Clientes Cadastrados"
)

try:

    df = pd.read_sql_query(
        """
        SELECT *
        FROM clientes
        ORDER BY id DESC
        """,
        conn
    )

    st.dataframe(
        df,
        use_container_width=True
    )

except Exception as erro:

    st.error(
        f"Erro ao carregar clientes: {erro}"
    )

conn.close()
