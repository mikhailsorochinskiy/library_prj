import re
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _


def validate_email(value):
    """
    Проверка email:
    - Формат email@domain.com
    - Недопустимые символы
    """
    if not value:
        raise ValidationError(
            _('Email не может быть пустым'),
            code='empty_email'
        )

    # Базовая проверка формата
    if not re.match(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$', value):
        raise ValidationError(
            _('Введите корректный email адрес'),
            code='invalid_email'
        )

    # Запрещенные домены (временные email)
    disposable_domains = ['tempmail.com', '10minutemail.com', 'guerrillamail.com']
    domain = value.split('@')[1]
    if domain in disposable_domains:
        raise ValidationError(
            _('Временные email адреса не разрешены'),
            code='disposable_email'
        )


# 2. Валидатор пароля (кастомный)
def validate_user_password(value):
    """
    Дополнительная проверка пароля:
    - Минимум 8 символов
    - Хотя бы одна заглавная буква
    - Хотя бы одна строчная буква
    - Хотя бы одна цифра
    - Хотя бы один спецсимвол
    """
    if len(value) < 8:
        raise ValidationError(
            _('Пароль должен содержать минимум 8 символов'),
            code='password_too_short'
        )

    if not re.search(r'[A-Z]', value):
        raise ValidationError(
            _('Пароль должен содержать хотя бы одну заглавную букву'),
            code='password_no_upper'
        )

    if not re.search(r'[a-z]', value):
        raise ValidationError(
            _('Пароль должен содержать хотя бы одну строчную букву'),
            code='password_no_lower'
        )

    if not re.search(r'[0-9]', value):
        raise ValidationError(
            _('Пароль должен содержать хотя бы одну цифру'),
            code='password_no_number'
        )


def validate_comment_text(value):
    """
    Проверка текста комментария:
    - Не пустой
    - Минимум 2 символа, максимум 1000
    - Не спам (не повторяющиеся символы)
    """
    if not value or not value.strip():
        raise ValidationError(
            _('Комментарий не может быть пустым'),
            code='empty_comment'
        )

    if len(value.strip()) < 2:
        raise ValidationError(
            _('Комментарий слишком короткий'),
            code='comment_too_short'
        )

    if len(value) > 1000:
        raise ValidationError(
            _('Комментарий не может превышать 1000 символов'),
            code='comment_too_long'
        )

    # Проверка на спам (повторяющиеся символы)
    if re.match(r'^(.)\1{5,}$', value.strip()):
        raise ValidationError(
            _('Комментарий не может состоять из повторяющихся символов'),
            code='comment_spam'
        )


class CommentValidator:
    def __call__(self, data):
        if 'text' in data:
            validate_comment_text(data['text'])
