from django.apps import AppConfig


class HomeConfig(AppConfig):
    default_auto_field: str = "django.db.models.AutoField"
    name = "{{ project_name }}.apps.home"
