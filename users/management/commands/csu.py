from django.core.management.base import BaseCommand
from users.models import User


class Command(BaseCommand):
    help = 'Создание суперпользователя'

    def handle(self, *args, **options):
        email = 'admin@mail.ru'

        # Проверяем, есть ли уже такой пользователь
        if not User.objects.filter(email=email).exists():
            # Создаем суперпользователя специальным методом
            User.objects.create_superuser(
                email=email,
                password='admin',
                username='admin'
            )
            self.stdout.write(self.style.SUCCESS(f'✅ Суперпользователь {email} успешно создан!'))
        else:
            self.stdout.write(self.style.WARNING(f'ℹ️ Суперпользователь {email} уже существует.'))