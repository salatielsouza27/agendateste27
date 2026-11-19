import streamlit as st
import sqlite3
import pandas as pd

st.set_page_config(
    page_title="Dashboard Executivo",
    layout="wide"
)

st.title("📊 Dashboard Executivo")

conn = sqlite3.connect(
    "beautyschedule.db",
    check_same_thread=False
)

# ==========================
# GARANTIR TABELAS
# ==========================

conn.execute("""
CREATE TABLE IF NOT EXISTS clientes (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nome TEXT
)
""")

conn.execute("""
CREATE TABLE IF NOT EXISTS profissionais (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nome TEXT
)
""")

conn.execute("""
CREATE TABLE IF NOT EXISTS servicos (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nome TEXT,
    valor REAL
)
""")

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

# ==========================
# INDICADORES
# ==========================

clientes = conn.execute(
    "SELECT COUNT(*) FROM clientes"
).fetchone()[0]

profissionais = conn.execute(
    "SELECT COUNT(*) FROM profissionais"
).fetchone()[0]

servicos = conn.execute(
    "SELECT COUNT(*) FROM servicos"
).fetchone()[0]

agendamentos = conn.execute(
    "SELECT COUNT(*) FROM agendamentos"
).fetchone()[0]

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(
        "Clientes",
        clientes
    )

with col2:
    st.metric(
        "Profissionais",
        profissionais
    )

with col3:
    st.metric(
        "Serviços",
        servicos
    )

with col4:
    st.metric(
        "Agendamentos",
        agendamentos
    )

st.divider()

# ==========================
# PRÓXIMOS AGENDAMENTOS
# ==========================

st.subheader(
    "📅 Próximos Agendamentos"
)

df_agenda = pd.read_sql_query(
    """
    SELECT
    cliente,
    profissional,
    servico,
    data,
    hora,
    status
    FROM agendamentos
    ORDER BY data,hora
    """,
    conn
)

if len(df_agenda) > 0:

    st.dataframe(
        df_agenda,
        use_container_width=True
    )

else:

    st.info(
        "Nenhum agendamento encontrado."
    )

st.divider()

# ==========================
# SERVIÇOS MAIS AGENDADOS
# ==========================

st.subheader(
    "🏆 Serviços Mais Agendados"
)

df_servicos = pd.read_sql_query(
    """
    SELECT
        servico,
        COUNT(*) quantidade
    FROM agendamentos
    GROUP BY servico
    ORDER BY quantidade DESC
    """,
    conn
)

if len(df_servicos) > 0:

    st.bar_chart(
        df_servicos.set_index(
            "servico"
        )
    )

else:

    st.info(
        "Sem dados suficientes."
    )

st.divider()

# ==========================
# PROFISSIONAIS MAIS OCUPADOS
# ==========================

st.subheader(
    "👨‍💼 Profissionais Mais Agendados"
)

df_profissionais = pd.read_sql_query(
    """
    SELECT
        profissional,
        COUNT(*) quantidade
    FROM agendamentos
    GROUP BY profissional
    ORDER BY quantidade DESC
    """,
    conn
)

if len(df_profissionais) > 0:

    st.bar_chart(
        df_profissionais.set_index(
            "profissional"
        )
    )

else:

    st.info(
        "Sem dados suficientes."
    )

st.divider()

# ==========================
# RESUMO FINANCEIRO
# ==========================

st.subheader(
    "💰 Resumo Financeiro"
)

try:

    valor_total = conn.execute(
        """
        SELECT SUM(valor)
        FROM servicos
        """
    ).fetchone()[0]

    valor_total = valor_total or 0

    st.metric(
        "Faturamento Potencial",
        f"R$ {valor_total:,.2f}"
    )

except:

    st.metric(
        "Faturamento Potencial",
        "R$ 0,00"
    )

conn.close()
