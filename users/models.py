from django.db import models
from django.contrib.auth.models import AbstractUser
from library.models import Book, Author


class User(AbstractUser):
    username = models.CharField(max_length=150, blank=True, null=True)
    email = models.EmailField(unique=True, verbose_name='Email')
    avatar = models.ImageField(upload_to='avatars', blank=True, null=True, verbose_name="Аватар",
                               help_text='Загрузите фото для вашей аватарки')
    points = models.IntegerField(default=0, verbose_name="Баллы")

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    def __str__(self):
        return f'{self.email}'


class SelectedBook(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name="book")

    class Meta:
        verbose_name = 'Избранная книга'
        verbose_name_plural = 'Избранные книги'

    def __str__(self):
        return f'Книга {self.book} добавлена в избранное у пользователя {self.user}'


class SubscribeAuthor(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    author = models.ForeignKey(Author, on_delete=models.CASCADE, related_name="author")

    class Meta:
        verbose_name = 'Подписка на автора'
        verbose_name_plural = 'Подписки на автора'

    def __str__(self):
        return f'Пользователь {self.user} подписался на автора {self.author}'
