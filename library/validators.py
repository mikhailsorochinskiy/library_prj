import re
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from django.core.validators import RegexValidator, MinLengthValidator, MaxLengthValidator


# 1. Валидатор имени автора
def validate_author_name(value):
    """
    Проверка имени автора:
    - Не пустое
    - Не содержит цифр
    - Не содержит спецсимволов кроме точки, дефиса и пробела
    - Минимум 2 символа
    """
    if len(value.strip()) < 2:
        raise ValidationError(
            _('Имя автора должно содержать минимум 2 символа'),
            code='min_length'
        )

    if any(char.isdigit() for char in value):
        raise ValidationError(
            _('Имя автора не должно содержать цифры'),
            code='contains_digits'
        )

    # Разрешенные символы: буквы, пробел, точка, дефис
    if not re.match(r'^[а-яА-Яa-zA-Z\s\.\-]+$', value):
        raise ValidationError(
            _('Имя автора может содержать только буквы, пробелы, точки и дефисы'),
            code='invalid_chars'
        )

    # Проверка на инициалы (например, "Пушкин А.С.")
    if '.' in value:
        parts = value.split()
        for part in parts:
            if '.' in part and len(part) > 3:
                raise ValidationError(
                    _('Инициалы должны быть в формате "А.С." (буква + точка)'),
                    code='invalid_initials'
                )


# 2. Валидатор биографии
def validate_bio(value):
    """
    Проверка биографии:
    - Не слишком короткая (мин 20 символов если указана)
    - Не слишком длинная (макс 5000 символов)
    """
    if value and len(value.strip()) < 20:
        raise ValidationError(
            _('Биография должна содержать минимум 20 символов'),
            code='bio_too_short'
        )

    if value and len(value) > 5000:
        raise ValidationError(
            _('Биография не может превышать 5000 символов'),
            code='bio_too_long'
        )


# 3. Класс-валидатор для автора
class AuthorValidator:
    def __init__(self, name=None, bio=None):
        self.name = name
        self.bio = bio

    def __call__(self, data):
        if 'name' in data:
            validate_author_name(data['name'])
        if 'bio' in data:
            validate_bio(data['bio'])


def validate_book_title(value):
    """
    Проверка названия книги:
    - Не пустое
    - Минимум 1 символ, максимум 200
    - Не может состоять только из пробелов
    """
    if not value or not value.strip():
        raise ValidationError(
            _('Название книги не может быть пустым'),
            code='empty_title'
        )

    if len(value) > 200:
        raise ValidationError(
            _('Название книги не может превышать 200 символов'),
            code='title_too_long'
        )

    if len(value.strip()) < 3:
        raise ValidationError(
            _('Название книги слишком короткое (минимум 3 символа)'),
            code='title_too_short'
        )


# 3. Валидатор жанра
def validate_genre(value):
    """
    Проверка жанра:
    - Только буквы, пробелы и дефисы
    - Первая буква заглавная
    """
    if value and not re.match(r'^[а-яА-Яa-zA-Z\s\-]+$', value):
        raise ValidationError(
            _('Жанр может содержать только буквы, пробелы и дефисы'),
            code='invalid_genre'
        )

    if value and value[0].islower():
        raise ValidationError(
            _('Жанр должен начинаться с заглавной буквы'),
            code='genre_capitalize'
        )


# 4. Валидатор читательской диспозиции
def validate_disposition(value):
    """
    Проверка диспозиции:
    - Должна быть из списка DISPOSITION_CHOICES
    """
    from .models import Book

    valid_choices = [choice[0] for choice in Book.DISPOSITION_CHOICES]
    if value and value not in valid_choices:
        raise ValidationError(
            _('Недопустимая читательская диспозиция. Выберите из: %(choices)s'),
            code='invalid_disposition',
            params={'choices': ', '.join(valid_choices)}
        )


# 5. Валидатор ссылки на текст
def validate_text_link(value):
    """
    Проверка ссылки на текст книги
    """
    if value and value != 'Ссылка на Текст книги временно недоступен':
        import re
        url_pattern = re.compile(
            r'^https?://'  # http:// или https://
            r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+[A-Z]{2,6}\.?|'  # домен
            r'localhost|'  # localhost
            r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})'  # IP
            r'(?::\d+)?'  # опциональный порт
            r'(?:/?|[/?]\S+)$', re.IGNORECASE)

        if not url_pattern.match(value):
            raise ValidationError(
                _('Введите корректный URL-адрес'),
                code='invalid_url'
            )

def validate_text_file_size(value):
    """
    Проверка размера файла (макс 50 МБ)
    """
    max_size = 50 * 1024 * 1024  # 50 МБ в байтах

    if value.size > max_size:
        raise ValidationError(
            _(f'Файл слишком большой. Максимальный размер: 50 МБ'),
            params={'max_size': '50 МБ'},
        )
