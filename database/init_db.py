import bcrypt

from database.connection import engine
from database.connection import SessionLocal

from database.models import (
    Base,
    User,
    Cliente,
    Profissional,
    Servico
)


def criar_admin():

    db = SessionLocal()

    admin = db.query(User).filter(
        User.email == "admin@beauty.com"
    ).first()

    if not admin:

        senha = bcrypt.hashpw(
            "123456".encode(),
            bcrypt.gensalt()
        ).decode()

        novo_admin = User(
            nome="Administrador",
            email="admin@beauty.com",
            senha=senha,
            perfil="ADMIN"
        )

        db.add(novo_admin)

    if db.query(Profissional).count() == 0:

        profissionais = [
            Profissional(
                nome="Fernanda",
                especialidade="Escova"
            ),
            Profissional(
                nome="Larissa",
                especialidade="Corte Feminino"
            ),
            Profissional(
                nome="Patricia",
                especialidade="Coloração"
            )
        ]

        db.add_all(profissionais)

    if db.query(Servico).count() == 0:

        servicos = [
            Servico(
                nome="Escova",
                valor=80,
                duracao=60
            ),
            Servico(
                nome="Corte Feminino",
                valor=60,
                duracao=45
            ),
            Servico(
                nome="Progressiva",
                valor=250,
                duracao=180
            )
        ]

        db.add_all(servicos)

    if db.query(Cliente).count() == 0:

        clientes = [
            Cliente(
                nome="Ana Souza",
                telefone="62999999999"
            ),
            Cliente(
                nome="Maria Oliveira",
                telefone="62988888888"
            ),
            Cliente(
                nome="Juliana Santos",
                telefone="62977777777"
            )
        ]

        db.add_all(clientes)

    db.commit()
    db.close()


def criar_banco():

    Base.metadata.create_all(
        bind=engine
    )

    criar_admin()


if __name__ == "__main__":

    criar_banco()

    print("Banco criado com sucesso")
