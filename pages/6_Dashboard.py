import streamlit as st
import pandas as pd

from sqlalchemy import func

from database.connection import SessionLocal
from database.models import (
    Cliente,
    Profissional,
    Servico,
    Agendamento
)

st.set_page_config(
    page_title="Dashboard",
    layout="wide"
)

db = SessionLocal()

st.title("Dashboard Executivo")

# =====================================
# MÉTRICAS PRINCIPAIS
# =====================================

total_clientes = db.query(
    Cliente
).count()

total_profissionais = db.query(
    Profissional
).count()

total_servicos = db.query(
    Servico
).count()

total_agendamentos = db.query(
    Agendamento
).count()

# =====================================
# FATURAMENTO
# =====================================

resultado = (
    db.query(
        func.sum(Servico.valor)
    )
    .join(
        Agendamento,
        Agendamento.servico_id == Servico.id
    )
    .scalar()
)

faturamento = resultado or 0

# =====================================
# CARDS
# =====================================

c1, c2, c3, c4, c5 = st.columns(5)

with c1:
    st.metric(
        "Clientes",
        total_clientes
    )

with c2:
    st.metric(
        "Profissionais",
        total_profissionais
    )

with c3:
    st.metric(
        "Serviços",
        total_servicos
    )

with c4:
    st.metric(
        "Agendamentos",
        total_agendamentos
    )

with c5:
    st.metric(
        "Faturamento",
        f"R$ {faturamento:.2f}"
    )

st.divider()

# =====================================
# PRÓXIMOS AGENDAMENTOS
# =====================================

st.subheader(
    "Próximos Agendamentos"
)

agendamentos = db.query(
    Agendamento
).all()

dados = []

for ag in agendamentos:

    cliente = db.query(
        Cliente
    ).get(
        ag.cliente_id
    )

    profissional = db.query(
        Profissional
    ).get(
        ag.profissional_id
    )

    servico = db.query(
        Servico
    ).get(
        ag.servico_id
    )

    dados.append({

        "Cliente":
        cliente.nome,

        "Profissional":
        profissional.nome,

        "Serviço":
        servico.nome,

        "Data":
        ag.data,

        "Hora":
        ag.hora,

        "Status":
        ag.status

    })

if dados:

    df = pd.DataFrame(
        dados
    )

    st.dataframe(
        df,
        use_container_width=True
    )

else:

    st.info(
        "Nenhum agendamento encontrado"
    )

st.divider()

# =====================================
# SERVIÇOS MAIS VENDIDOS
# =====================================

st.subheader(
    "Serviços Mais Agendados"
)

servicos_populares = []

servicos = db.query(
    Servico
).all()

for servico in servicos:

    quantidade = db.query(
        Agendamento
    ).filter(
        Agendamento.servico_id
        == servico.id
    ).count()

    servicos_populares.append({

        "Serviço":
        servico.nome,

        "Quantidade":
        quantidade

    })

if servicos_populares:

    grafico = pd.DataFrame(
        servicos_populares
    )

    st.bar_chart(
        grafico.set_index(
            "Serviço"
        )
    )

st.divider()

# =====================================
# PROFISSIONAIS MAIS OCUPADOS
# =====================================

st.subheader(
    "Profissionais Mais Agendados"
)

profissionais_dashboard = []

profissionais = db.query(
    Profissional
).all()

for profissional in profissionais:

    quantidade = db.query(
        Agendamento
    ).filter(
        Agendamento.profissional_id
        == profissional.id
    ).count()

    profissionais_dashboard.append({

        "Profissional":
        profissional.nome,

        "Agendamentos":
        quantidade

    })

if profissionais_dashboard:

    grafico_profissionais = pd.DataFrame(
        profissionais_dashboard
    )

    st.bar_chart(
        grafico_profissionais.set_index(
            "Profissional"
        )
    )

db.close()
