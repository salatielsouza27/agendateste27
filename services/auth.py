import bcrypt
from sqlalchemy.orm import Session

from database.models import User


def criar_hash(senha: str):
    return bcrypt.hashpw(
        senha.encode(),
        bcrypt.gensalt()
    ).decode()


def verificar_senha(
    senha_digitada: str,
    senha_hash: str
):
    return bcrypt.checkpw(
        senha_digitada.encode(),
        senha_hash.encode()
    )


def autenticar_usuario(
    db: Session,
    email: str,
    senha: str
):

    usuario = db.query(User).filter(
        User.email == email
    ).first()

    if not usuario:
        return None

    if not verificar_senha(
        senha,
        usuario.senha
    ):
        return None

    return usuario
