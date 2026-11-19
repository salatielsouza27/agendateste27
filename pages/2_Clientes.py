import streamlit as st
import pandas as pd

from database.connection import SessionLocal
from database.models import Cliente

st.set_page_config(
    page_title="Clientes",
    layout="wide"
)

db = SessionLocal()

st.title("Cadastro de Clientes")

# =====================
# NOVO CLIENTE
# =====================

with st.expander("Novo Cliente", expanded=True):

    with st.form("novo_cliente"):

        nome = st.text_input("Nome")

        telefone = st.text_input("Telefone")

        email = st.text_input("E-mail")

        observacoes = st.text_area("Observações")

        salvar = st.form_submit_button(
            "Salvar Cliente"
        )

        if salvar:

            if nome.strip() == "":
                st.error("Informe o nome")
            else:

                cliente = Cliente(
                    nome=nome,
                    telefone=telefone,
                    email=email,
                    observacoes=observacoes
                )

                db.add(cliente)
                db.commit()

                st.success(
                    "Cliente cadastrado com sucesso"
                )

                st.rerun()

# =====================
# LISTAGEM
# =====================

st.subheader("Clientes Cadastrados")

clientes = db.query(
    Cliente
).order_by(
    Cliente.nome
).all()

dados = []

for c in clientes:

    dados.append({
        "ID": c.id,
        "Nome": c.nome,
        "Telefone": c.telefone,
        "Email": c.email
    })

df = pd.DataFrame(dados)

if not df.empty:
    st.dataframe(
        df,
        use_container_width=True
    )
else:
    st.info(
        "Nenhum cliente encontrado"
    )

# =====================
# EDITAR
# =====================

st.divider()

st.subheader("Editar Cliente")

if clientes:

    cliente_id = st.selectbox(
        "Selecione",
        options=[
            c.id
            for c in clientes
        ]
    )

    cliente = db.query(
        Cliente
    ).filter(
        Cliente.id == cliente_id
    ).first()

    with st.form("editar_cliente"):

        novo_nome = st.text_input(
            "Nome",
            value=cliente.nome
        )

        novo_telefone = st.text_input(
            "Telefone",
            value=cliente.telefone or ""
        )

        novo_email = st.text_input(
            "Email",
            value=cliente.email or ""
        )

        nova_obs = st.text_area(
            "Observações",
            value=cliente.observacoes or ""
        )

        atualizar = st.form_submit_button(
            "Atualizar"
        )

        if atualizar:

            cliente.nome = novo_nome
            cliente.telefone = novo_telefone
            cliente.email = novo_email
            cliente.observacoes = nova_obs

            db.commit()

            st.success(
                "Cliente atualizado"
            )

            st.rerun()

# =====================
# EXCLUIR
# =====================

st.divider()

st.subheader("Excluir Cliente")

if clientes:

    excluir_id = st.selectbox(
        "Cliente para excluir",
        options=[
            c.id
            for c in clientes
        ],
        key="delete"
    )

    if st.button(
        "Excluir Cliente",
        type="primary"
    ):

        cliente = db.query(
            Cliente
        ).filter(
            Cliente.id == excluir_id
        ).first()

        db.delete(cliente)

        db.commit()

        st.success(
            "Cliente removido"
        )

        st.rerun()

db.close()
