from django.core.management.base import BaseCommand

from users.models import User


class Command(BaseCommand):
    def handle(self, *args, **options):
        user = User.objects.filter(email='admin@mail.ru')
        if not user.exists():
            user = User.objects.filter(email='admin@mail.ru')
            user.set_password('admin')
            user.is_active = True
            user.is_staff = True
            user.is_superuser = True
            user.save()
