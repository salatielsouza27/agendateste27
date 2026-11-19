import streamlit as st

from database.connection import SessionLocal
from services.auth import autenticar_usuario

st.set_page_config(
    page_title="Login",
    layout="centered"
)

if "logado" not in st.session_state:
    st.session_state.logado = False

if "usuario" not in st.session_state:
    st.session_state.usuario = None

st.title("BeautySchedule")

if not st.session_state.logado:

    with st.form("login"):

        email = st.text_input(
            "E-mail"
        )

        senha = st.text_input(
            "Senha",
            type="password"
        )

        entrar = st.form_submit_button(
            "Entrar"
        )

        if entrar:

            db = SessionLocal()

            usuario = autenticar_usuario(
                db,
                email,
                senha
            )

            db.close()

            if usuario:

                st.session_state.logado = True

                st.session_state.usuario = {
                    "id": usuario.id,
                    "nome": usuario.nome,
                    "perfil": usuario.perfil
                }

                st.success(
                    "Login realizado com sucesso"
                )

                st.rerun()

            else:

                st.error(
                    "Usuário ou senha inválidos"
                )

else:

    st.success(
        f"Bem-vindo {st.session_state.usuario['nome']}"
    )

    st.write(
        f"Perfil: {st.session_state.usuario['perfil']}"
    )

    if st.button("Logout"):

        st.session_state.logado = False
        st.session_state.usuario = None

        st.rerun()
