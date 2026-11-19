import streamlit as st
import pandas as pd

from database.connection import SessionLocal
from database.models import Servico

st.set_page_config(
    page_title="Serviços",
    layout="wide"
)

db = SessionLocal()

st.title("Cadastro de Serviços")

# =====================================
# NOVO SERVIÇO
# =====================================

with st.expander(
    "Novo Serviço",
    expanded=True
):

    with st.form("novo_servico"):

        nome = st.text_input(
            "Nome do Serviço"
        )

        descricao = st.text_area(
            "Descrição"
        )

        duracao = st.number_input(
            "Duração (Minutos)",
            min_value=1,
            value=60
        )

        valor = st.number_input(
            "Valor (R$)",
            min_value=0.0,
            step=1.0
        )

        ativo = st.checkbox(
            "Ativo",
            value=True
        )

        salvar = st.form_submit_button(
            "Salvar Serviço"
        )

        if salvar:

            if nome.strip() == "":

                st.error(
                    "Informe o nome do serviço"
                )

            else:

                servico = Servico(
                    nome=nome,
                    descricao=descricao,
                    duracao=duracao,
                    valor=valor,
                    ativo=ativo
                )

                db.add(servico)

                db.commit()

                st.success(
                    "Serviço cadastrado com sucesso"
                )

                st.rerun()

# =====================================
# LISTAGEM
# =====================================

st.divider()

st.subheader(
    "Serviços Cadastrados"
)

servicos = db.query(
    Servico
).order_by(
    Servico.nome
).all()

dados = []

for s in servicos:

    dados.append({
        "ID": s.id,
        "Serviço": s.nome,
        "Descrição": s.descricao,
        "Duração": f"{s.duracao} min",
        "Valor": f"R$ {s.valor:.2f}",
        "Ativo": "Sim" if s.ativo else "Não"
    })

df = pd.DataFrame(dados)

if not df.empty:

    st.dataframe(
        df,
        use_container_width=True
    )

else:

    st.info(
        "Nenhum serviço cadastrado"
    )

# =====================================
# EDITAR
# =====================================

st.divider()

st.subheader(
    "Editar Serviço"
)

if servicos:

    servico_id = st.selectbox(
        "Selecione o Serviço",
        options=[
            s.id
            for s in servicos
        ]
    )

    servico = db.query(
        Servico
    ).filter(
        Servico.id == servico_id
    ).first()

    with st.form(
        "editar_servico"
    ):

        nome_edit = st.text_input(
            "Nome",
            value=servico.nome
        )

        descricao_edit = st.text_area(
            "Descrição",
            value=servico.descricao or ""
        )

        duracao_edit = st.number_input(
            "Duração",
            value=servico.duracao
        )

        valor_edit = st.number_input(
            "Valor",
            value=float(servico.valor)
        )

        ativo_edit = st.checkbox(
            "Ativo",
            value=servico.ativo
        )

        atualizar = st.form_submit_button(
            "Atualizar"
        )

        if atualizar:

            servico.nome = nome_edit
            servico.descricao = descricao_edit
            servico.duracao = duracao_edit
            servico.valor = valor_edit
            servico.ativo = ativo_edit

            db.commit()

            st.success(
                "Serviço atualizado"
            )

            st.rerun()

# =====================================
# EXCLUIR
# =====================================

st.divider()

st.subheader(
    "Excluir Serviço"
)

if servicos:

    excluir_id = st.selectbox(
        "Serviço para excluir",
        options=[
            s.id
            for s in servicos
        ],
        key="servico_delete"
    )

    if st.button(
        "Excluir Serviço",
        type="primary"
    ):

        servico = db.query(
            Servico
        ).filter(
            Servico.id == excluir_id
        ).first()

        db.delete(
            servico
        )

        db.commit()

        st.success(
            "Serviço removido com sucesso"
        )

        st.rerun()

db.close()
