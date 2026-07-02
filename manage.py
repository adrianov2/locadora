#!/usr/bin/env python
import os
import sys


def create_superuser():
    """
    Cria um superusuário automaticamente caso ainda não exista.
    """

    try:
        import django

        django.setup()

        from django.contrib.auth import get_user_model

        User = get_user_model()

        username = os.getenv("DJANGO_SUPERUSER_USERNAME")
        email = os.getenv("DJANGO_SUPERUSER_EMAIL")
        password = os.getenv("DJANGO_SUPERUSER_PASSWORD")

        if username and password:
            if not User.objects.filter(username=username).exists():
                User.objects.create_superuser(
                    username=username,
                    email=email,
                    password=password,
                )
                print("✅ Superusuário criado com sucesso!")
            else:
                print("ℹ️ Superusuário já existe.")

    except Exception as e:
        print(f"Erro ao criar superusuário: {e}")


def main():
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "core.settings")

    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. "
            "Are you sure it's installed?"
        ) from exc

    if len(sys.argv) > 1 and sys.argv[1] == "runserver":
        create_superuser()

    execute_from_command_line(sys.argv)


if __name__ == "__main__":
    main()