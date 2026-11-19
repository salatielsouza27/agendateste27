import streamlit as st
import pandas as pd
import sqlite3

st.set_page_config(
    page_title="Clientes",
    layout="wide"
)

st.title("Cadastro de Clientes")

conn = sqlite3.connect(
    "beautyschedule.db",
    check_same_thread=False
)

# Cria tabela automaticamente
conn.execute("""
CREATE TABLE IF NOT EXISTS clientes (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nome TEXT NOT NULL,
    telefone TEXT,
    email TEXT,
    observacoes TEXT
)
""")

# ===============================
# NOVO CLIENTE
# ===============================

with st.expander(
    "Novo Cliente",
    expanded=True
):

    with st.form("cliente_form"):

        nome = st.text_input("Nome")

        telefone = st.text_input("Telefone")

        email = st.text_input("E-mail")

        observacoes = st.text_area(
            "Observações"
        )

        salvar = st.form_submit_button(
            "Salvar Cliente"
        )

        if salvar:

            if nome.strip() == "":

                st.error(
                    "Informe o nome do cliente"
                )

            else:

                conn.execute(
                    """
                    INSERT INTO clientes
                    (
                        nome,
                        telefone,
                        email,
                        observacoes
                    )
                    VALUES
                    (?, ?, ?, ?)
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
                    "Cliente cadastrado com sucesso"
                )

                st.rerun()

# ===============================
# CLIENTES CADASTRADOS
# ===============================

st.divider()

st.subheader(
    "Clientes Cadastrados"
)

df = pd.read_sql_query(
    """
    SELECT
    id,
    nome,
    telefone,
    email
    FROM clientes
    ORDER BY nome
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
        "Nenhum cliente cadastrado"
    )

# ===============================
# EXCLUIR CLIENTE
# ===============================

st.divider()

st.subheader(
    "Excluir Cliente"
)

if len(df) > 0:

    cliente_id = st.selectbox(
        "Selecione",
        df["id"]
    )

    if st.button(
        "Excluir Cliente"
    ):

        conn.execute(
            """
            DELETE FROM clientes
            WHERE id=?
            """,
            (int(cliente_id),)
        )

        conn.commit()

        st.success(
            "Cliente removido"
        )

        st.rerun()

conn.close()
