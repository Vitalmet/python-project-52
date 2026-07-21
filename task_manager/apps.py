from django.apps import AppConfig
from django.db.models.signals import post_migrate


def create_initial_data(sender, **kwargs):
    from django.contrib.auth.models import User
    from .models import Status

    # Создаем пользователей если их нет
    if User.objects.count() < 2:
        User.objects.create_user(
            username="testuser",
            password="testpass123",
            first_name="Test",
            last_name="User"
        )
        User.objects.create_user(
            username="executor",
            password="testpass123",
            first_name="Executor",
            last_name="User"
        )
        print("Created test users")

    # Создаем статусы если их нет
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
