from django.db import models
from django.core.validators import FileExtensionValidator
from .validators import (validate_author_name, validate_bio, validate_book_title,
                         validate_genre, validate_disposition, validate_text_file_size)
import os


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

    text_file = models.FileField(
        upload_to='books/texts/%Y/%m/%d/',  # Папки по годам/месяцам/дням
        verbose_name="Файл с текстом книги",
        blank=True,
        null=True,
        validators=[
            FileExtensionValidator(
                allowed_extensions=['pdf', 'txt', 'epub', 'fb2', 'docx', 'rtf'],
                message='Поддерживаются только: PDF, TXT, EPUB, FB2, DOCX, RTF'
            ),
            validate_text_file_size  # Кастомный валидатор размера
        ],
        help_text="Загрузите файл с текстом книги (макс. 50 МБ)"
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Книга'
        verbose_name_plural = 'Книги'

    def __str__(self):
        return f"{self.title} - {self.author.name}"

    def has_text(self):
        """Проверяет, есть ли загруженный текст"""
        return bool(self.text_file)

    has_text.boolean = True
    has_text.short_description = "Текст загружен"

    def get_text_url(self):
        """Возвращает URL для доступа к файлу"""
        if self.text_file:
            return self.text_file.url
        return None

    def get_file_size(self):
        """Возвращает размер файла в человекочитаемом формате"""
        if self.text_file and self.text_file.size:
            size = self.text_file.size
            for unit in ['Б', 'КБ', 'МБ', 'ГБ']:
                if size < 1024.0:
                    return f"{size:.1f} {unit}"
                size /= 1024.0
        return "0 Б"

    def get_file_extension(self):
        """Возвращает расширение файла"""
        if self.text_file:
            return os.path.splitext(self.text_file.name)[1].lower()
        return None
