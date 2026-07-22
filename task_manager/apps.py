from django.apps import AppConfig
from django.db.models.signals import post_migrate


def create_initial_data(sender, **kwargs):
    from .models import Status

    if Status.objects.count() == 0:
        Status.objects.create(name="Новый")
        Status.objects.create(name="В работе")
        Status.objects.create(name="Завершен")
        print("Created default statuses")


class TaskManagerConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'task_manager'

    def ready(self):
        post_migrate.connect(create_initial_data, sender=self)
