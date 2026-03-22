# users/management/commands/create_groups.py
from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from library.models import Book, Author
from users.models import User, Comment


class Command(BaseCommand):
    help = 'Создание групп и прав доступа'

    def handle(self, *args, **options):
        # Создаем группы
        readers_group, _ = Group.objects.get_or_create(name='Readers')
        moderators_group, _ = Group.objects.get_or_create(name='Moderators')

        # ===== ПРАВА ДЛЯ КНИГ =====
        book_content_type = ContentType.objects.get_for_model(Book)

        book_permissions = {
            'view': Permission.objects.get(
                content_type=book_content_type,
                codename='view_book'
            ),
            'add': Permission.objects.get(
                content_type=book_content_type,
                codename='add_book'
            ),
            'change': Permission.objects.get(
                content_type=book_content_type,
                codename='change_book'
            ),
            'delete': Permission.objects.get(
                content_type=book_content_type,
                codename='delete_book'
            ),
        }

        # ===== ПРАВА ДЛЯ АВТОРОВ =====
        author_content_type = ContentType.objects.get_for_model(Author)

        author_permissions = {
            'view': Permission.objects.get(
                content_type=author_content_type,
                codename='view_author'
            ),
            'add': Permission.objects.get(
                content_type=author_content_type,
                codename='add_author'
            ),
            'change': Permission.objects.get(
                content_type=author_content_type,
                codename='change_author'
            ),
            'delete': Permission.objects.get(
                content_type=author_content_type,
                codename='delete_author'
            ),
        }

        # ===== ПРАВА ДЛЯ КОММЕНТАРИЕВ =====
        comment_content_type = ContentType.objects.get_for_model(Comment)

        comment_permissions = {
            'view': Permission.objects.get(
                content_type=comment_content_type,
                codename='view_comment'
            ),
            'add': Permission.objects.get(
                content_type=comment_content_type,
                codename='add_comment'
            ),
            'change': Permission.objects.get(
                content_type=comment_content_type,
                codename='change_comment'
            ),
            'delete': Permission.objects.get(
                content_type=comment_content_type,
                codename='delete_comment'
            ),
        }

        # ===== НАЗНАЧАЕМ ПРАВА ГРУППАМ =====

        # Читатели: только просмотр книг/авторов + комментарии
        readers_group.permissions.add(
            book_permissions['view'],
            author_permissions['view'],
            comment_permissions['add'],  # могут добавлять комментарии
            comment_permissions['view'],  # могут видеть комментарии
        )

        # Модераторы: всё что читатели + добавление/изменение книг и авторов
        moderators_group.permissions.add(
            book_permissions['view'],
            book_permissions['add'],
            book_permissions['change'],
            author_permissions['view'],
            author_permissions['add'],
            author_permissions['change'],
            comment_permissions['view'],
            comment_permissions['delete'],  # могут удалять плохие комментарии
        )

        self.stdout.write(
            self.style.SUCCESS('✅ Группы и права успешно созданы')
        )