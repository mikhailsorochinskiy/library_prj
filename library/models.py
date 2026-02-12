from django.db import models
from .validators import (validate_author_name, validate_bio, validate_book_title,
                         validate_genre, validate_disposition, validate_text_link)


class Author(models.Model):
    name = models.CharField(max_length=100, validators=[validate_author_name], verbose_name="Имя автора")
    bio = models.TextField(blank=True, null=True, validators=[validate_bio], verbose_name="Биография")
    photo = models.ImageField(upload_to='authors/', null=True, blank=True)

    class Meta:
        verbose_name = 'Автор'
        verbose_name_plural = 'Авторы'

    def __str__(self):
        return self.name


class Book(models.Model):
    DISPOSITION_CHOICES = [
        ("Socializing", "Социализирующая"),
        ("Cultural-Educational", "Культурно-познавательная"),
        ("Aesthetic", "Эстетическая"),
        ("Emotional-Emphatic", "Эмоционально-эмпатическая"),
        ("Philosophical-Ideological", "Философско-мировоззренческая"),
        ("Existential", "Экзистенциальная"),
        ("Optimizing", "Оптимизирующая"),
        ("Entertaining", "Развлекательная"),
        ("Escapist", "Эскапическая"),
        ("Undifferentiated", "Недифференцированная"),
    ]

    title = models.CharField(max_length=200, validators=[validate_book_title], verbose_name="Название")
    author = models.ForeignKey(Author, on_delete=models.CASCADE, related_name="Author")
    description = models.TextField(verbose_name="Описание", blank=True, null=True)
    preview_image = models.ImageField(upload_to='book_covers/', blank=True, null=True, verbose_name="Превью")
    genre = models.CharField(max_length=50, verbose_name="Жанр", blank=True, null=True, validators=[validate_genre])
    disposition = models.CharField(max_length=50, choices=DISPOSITION_CHOICES, verbose_name="Читательская диспозиция",
                                   blank=True, null=True, validators=[validate_disposition],)

    text_link = models.TextField(
        blank=True,
        null=True,
        validators=[validate_text_link],
        default='Ссылка на Текст книги временно недоступен'
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Книга'
        verbose_name_plural = 'Книги'

    def __str__(self):
        return f"{self.title} - {self.author.name}"
