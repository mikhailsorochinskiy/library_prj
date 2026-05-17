from rest_framework import serializers
from .models import User, SelectedBook, SubscribeAuthor, Comment, Rating
from library.serializers import BookSerializer, AuthorSerializer
from library.models import Book, Author
from .validators import validate_user_password, validate_email
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.core.mail import send_mail
from django.conf import settings


class SelectedBookSerializer(serializers.ModelSerializer):
    book = BookSerializer(read_only=True)
    book_id = serializers.PrimaryKeyRelatedField(
        queryset=Book.objects.all(),
        source='book',
        write_only=True
    )

    class Meta:
        model = SelectedBook
        fields = ['id', 'book', 'book_id']


class SubscribeAuthorSerializer(serializers.ModelSerializer):
    author = AuthorSerializer(read_only=True)
    author_id = serializers.PrimaryKeyRelatedField(
        queryset=Author.objects.all(),
        source='author',
        write_only=True
    )

    class Meta:
        model = SubscribeAuthor
        fields = ['id', 'author', 'author_id']


class UserSerializer(serializers.ModelSerializer):
    is_moderator = serializers.BooleanField(read_only=True)
    role = serializers.SerializerMethodField()
    selected_books = SelectedBookSerializer(many=True, read_only=True)
    subscribes = SubscribeAuthorSerializer(many=True, read_only=True)

    password = serializers.CharField(
        write_only=True,
        required=False,  # Не обязателен при обновлении
        style={'input_type': 'password'},  # Для browsable API
        validators=[validate_user_password]  # Если есть валидатор
    )

    class Meta:
        model = User
        fields = ('id', 'email', 'password', 'points', 'selected_books', 'subscribes', 'is_moderator', 'role')
        read_only_fields = ('points', 'is_moderator')
        extra_kwargs = {
            'email': {
                'required': True,
                'validators': [validate_email]  # Если есть валидатор
            },
            'points': {
                'read_only': True,  # Баллы начисляются только через тесты
            },
            'password': {
                'write_only': True,  # Дублируем здесь для надежности
                'min_length': 8,
            }
        }

    def create(self, validated_data):
        password = validated_data.pop('password', None)
        # 1. Создаем пользователя, но пока блокируем вход (is_active=False)
        validated_data['is_active'] = False
        user = super().create(validated_data)

        if password:
            user.set_password(password)
            user.save()

        # 2. Генерируем токен и ID для ссылки
        uid = urlsafe_base64_encode(force_bytes(user.pk))
        token = default_token_generator.make_token(user)

        # 3. Формируем ссылку с использованием FRONTEND_URL
        verify_url = f"{settings.FRONTEND_URL}/verify-email/{uid}/{token}/"

        # 4. Отправляем письмо (пока упадет в консоль)
        send_mail(
            subject="Подтверждение регистрации",
            message=f"Добро пожаловать в нашу библиотеку!\n\nДля подтверждения почты перейдите по ссылке:\n{verify_url}",
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[user.email],
            fail_silently=True,
        )

        return user

    def get_role(self, obj):
        if obj.is_staff:
            return 'admin'
        elif obj.is_moderator:
            return 'moderator'
        else:
            return 'reader'


class CommentSerializer(serializers.ModelSerializer):

    class Meta:
        model = Comment
        fields = ('id', 'owner', 'book', 'text')


class RatingSerializer(serializers.ModelSerializer):

    class Meta:
        model = Rating
        fields = ('id', 'owner', 'book', 'rating')


class AddPointsSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)
    points = serializers.IntegerField(min_value=1, max_value=100)
