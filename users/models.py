from django.db import models
from django.contrib.auth.models import AbstractUser
from library.models import Book, Author
from .validators import validate_email, validate_comment_text
from django.core.validators import MinValueValidator, MaxValueValidator

class User(AbstractUser):
    username = models.CharField(max_length=150, blank=True, null=True)
    email = models.EmailField(unique=True, validators=[validate_email], verbose_name='Email')
    points = models.IntegerField(default=0, verbose_name="Баллы")
    is_tested = models.BooleanField(default=False, verbose_name="Прошел тест?")

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    @property
    def is_moderator(self):
        return self.groups.filter(name='Moderators').exists()

    def __str__(self):
        return f'{self.email}'


class SelectedBook(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="selected_books")
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name="book")

    class Meta:
        unique_together = ("user", "book")
        verbose_name = 'Избранная книга'
        verbose_name_plural = 'Избранные книги'

    def __str__(self):
        return f'Книга {self.book} добавлена в избранное у пользователя {self.user}'


class SubscribeAuthor(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="subscribes")
    author = models.ForeignKey(Author, on_delete=models.CASCADE, related_name="author")

    class Meta:
        unique_together = ("user", "author")
        verbose_name = 'Подписка на автора'
        verbose_name_plural = 'Подписки на автора'

    def __str__(self):
        return f'Пользователь {self.user} подписался на автора {self.author.name}'


class Comment(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    text = models.TextField(max_length=500, validators=[validate_comment_text], verbose_name="текст")

    def __str__(self):
        return f'{self.owner} оставил коммент под книгой {self.book}.'

    class Meta:
        verbose_name = 'Коммент'
        verbose_name_plural = 'Комменты'


class Rating(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    rating = models.IntegerField(verbose_name="оценка", validators=[
            MinValueValidator(1, message='Оценка не может быть меньше 1'),
            MaxValueValidator(10, message='Оценка не может быть больше 10')
        ])

    def __str__(self):
        return f'{self.owner} поставил оценку {self.rating} под книгой {self.book}.'

    class Meta:
        verbose_name = 'Оценка'
        verbose_name_plural = 'Оценки'
        unique_together = ['owner', 'book']


class ScoreLog(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)
    book = models.ForeignKey(Book, on_delete=models.SET_NULL, null=True)
    author = models.ForeignKey(Author, on_delete=models.SET_NULL, null=True)
    comment = models.BooleanField(default=False)
    rating = models.BooleanField(default=False)
    points = models.IntegerField()
