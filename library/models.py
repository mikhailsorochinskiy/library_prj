from django.db import models


class Author(models.Model):
    name = models.CharField(max_length=100)
    bio = models.TextField(blank=True)
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

    title = models.CharField(max_length=200, verbose_name="Название")
    author = models.ForeignKey(Author, on_delete=models.CASCADE, related_name="Author")
    description = models.TextField(verbose_name="Описание", blank=True, null=True)
    preview_image = models.ImageField(upload_to='book_covers/', blank=True, null=True, verbose_name="Превью")
    genre = models.CharField(max_length=50, verbose_name="Жанр", blank=True, null=True)
    disposition = models.CharField(max_length=50, choices=DISPOSITION_CHOICES, verbose_name="Читательская диспозиция",
                                   blank=True, null=True)

    text_link = models.TextField(
        blank=True,
        null=True,
        default='Ссылка на Текст книги временно недоступен'
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Книга'
        verbose_name_plural = 'Книги'

    def __str__(self):
        return f"{self.title} - {self.author.name}"
