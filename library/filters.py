import django_filters
from .models import Book


class BookFilter(django_filters.FilterSet):
    # Простой фильтр по точному совпадению жанра
    genre = django_filters.CharFilter(field_name='genre', lookup_expr='icontains')

    # Фильтр по нескольким диспозициям
    disposition = django_filters.MultipleChoiceFilter(
        field_name='disposition',
        choices=Book.DISPOSITION_CHOICES
    )

    # Фильтр по автору (по ID)
    author = django_filters.NumberFilter(field_name='author__id')

    # Фильтр по имени автора
    author_name = django_filters.CharFilter(
        field_name='author__name',
        lookup_expr='icontains'
    )

    class Meta:
        model = Book
        fields = ['genre', 'disposition', 'author']
