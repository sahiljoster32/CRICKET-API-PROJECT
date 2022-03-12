from django.apps import AppConfig


class UserConfig(AppConfig):
    default_auto_field: str = 'django.db.models.BigAutoField'
    name: str = 'user'
