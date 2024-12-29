from django.apps import AppConfig


class DoctrisBaseConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'doctris_base'
