from django.apps import AppConfig


class NewsConfig(AppConfig):
    default_auto_field: str = "django.db.models.AutoField"
    name = "{{ project_name }}.apps.news"
