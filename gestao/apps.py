from django.apps import AppConfig


class GestaoConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "gestao"

    def ready(self):
        try:
            from .startup import criar_superusuario
            criar_superusuario()
        except Exception as e:
            print(f"Erro ao criar superusuário: {e}")