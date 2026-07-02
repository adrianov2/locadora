import os

from django.contrib.auth import get_user_model
from django.db import OperationalError, ProgrammingError


def criar_superusuario():
    try:
        User = get_user_model()

        username = os.getenv("ADMIN_USERNAME")
        email = os.getenv("ADMIN_EMAIL")
        password = os.getenv("ADMIN_PASSWORD")

        if not username or not password:
            return

        if not User.objects.filter(username=username).exists():

            User.objects.create_superuser(
                username=username,
                email=email,
                password=password,
                perfil="admin",
            )

            print("=" * 50)
            print("SUPERUSUÁRIO CRIADO")
            print("=" * 50)

    except (OperationalError, ProgrammingError):
        # Banco ainda não existe ou migrações não terminaram
        pass