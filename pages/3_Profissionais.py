import streamlit as st
import pandas as pd

from database.connection import SessionLocal
from database.models import Profissional

st.set_page_config(
    page_title="Profissionais",
    layout="wide"
)

db = SessionLocal()

st.title("Cadastro de Profissionais")

# =================================
# NOVO PROFISSIONAL
# =================================

with st.expander(
    "Novo Profissional",
    expanded=True
):

    with st.form("novo_profissional"):

        nome = st.text_input(
            "Nome"
        )

        telefone = st.text_input(
            "Telefone"
        )

        especialidade = st.text_input(
            "Especialidade"
        )

        ativo = st.checkbox(
            "Ativo",
            value=True
        )

        salvar = st.form_submit_button(
            "Salvar"
        )

        if salvar:

            if nome.strip() == "":

                st.error(
                    "Informe o nome"
                )

            else:

                profissional = Profissional(
                    nome=nome,
                    telefone=telefone,
                    especialidade=especialidade,
                    ativo=ativo
                )

                db.add(profissional)

                db.commit()

                st.success(
                    "Profissional cadastrado"
                )

                st.rerun()

# =================================
# LISTAGEM
# =================================

st.divider()

st.subheader(
    "Profissionais Cadastrados"
)

profissionais = db.query(
    Profissional
).order_by(
    Profissional.nome
).all()

dados = []

for p in profissionais:

    dados.append({
        "ID": p.id,
        "Nome": p.nome,
        "Telefone": p.telefone,
        "Especialidade": p.especialidade,
        "Ativo": "Sim" if p.ativo else "Não"
    })

df = pd.DataFrame(dados)

if not df.empty:

    st.dataframe(
        df,
        use_container_width=True
    )

else:

    st.info(
        "Nenhum profissional cadastrado"
    )

# =================================
# EDITAR
# =================================

st.divider()

st.subheader(
    "Editar Profissional"
)

if profissionais:

    profissional_id = st.selectbox(
        "Selecione o profissional",
        options=[
            p.id
            for p in profissionais
        ]
    )

    profissional = db.query(
        Profissional
    ).filter(
        Profissional.id == profissional_id
    ).first()

    with st.form(
        "editar_profissional"
    ):

        nome_edit = st.text_input(
            "Nome",
            value=profissional.nome
        )

        telefone_edit = st.text_input(
            "Telefone",
            value=profissional.telefone or ""
        )

        especialidade_edit = st.text_input(
            "Especialidade",
            value=profissional.especialidade or ""
        )

        ativo_edit = st.checkbox(
            "Ativo",
            value=profissional.ativo
        )

        atualizar = st.form_submit_button(
            "Atualizar"
        )

        if atualizar:

            profissional.nome = nome_edit

            profissional.telefone = telefone_edit

            profissional.especialidade = especialidade_edit

            profissional.ativo = ativo_edit

            db.commit()

            st.success(
                "Profissional atualizado"
            )

            st.rerun()

# =================================
# EXCLUIR
# =================================

st.divider()

st.subheader(
    "Excluir Profissional"
)

if profissionais:

    excluir_id = st.selectbox(
        "Profissional para excluir",
        options=[
            p.id
            for p in profissionais
        ],
        key="excluir_profissional"
    )

    if st.button(
        "Excluir Profissional",
        type="primary"
    ):

        profissional = db.query(
            Profissional
        ).filter(
            Profissional.id == excluir_id
        ).first()

        db.delete(
            profissional
        )

        db.commit()

        st.success(
            "Profissional removido"
        )

        st.rerun()

db.close()
