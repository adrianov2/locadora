#!/usr/bin/env python
import os
import sys


def criar_superusuario():
    from django.contrib.auth import get_user_model

    User = get_user_model()

    username = os.getenv("ADMIN_USERNAME")
    email = os.getenv("ADMIN_EMAIL")
    password = os.getenv("ADMIN_PASSWORD")

    if not username or not password:
        return

    if not User.objects.filter(username=username).exists():
        print("Criando superusuário...")

        User.objects.create_superuser(
            username=username,
            email=email,
            password=password,
        )

        print("Superusuário criado com sucesso!")
    else:
        print("Superusuário já existe.")


def main():
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "core.settings")

    from django.core.management import execute_from_command_line

    execute_from_command_line(sys.argv)

    if sys.argv[1:] and sys.argv[1] == "migrate":
        try:
            import django

            django.setup()

            criar_superusuario()

        except Exception as e:
            print("Erro ao criar superusuário:", e)


if __name__ == "__main__":
    main()