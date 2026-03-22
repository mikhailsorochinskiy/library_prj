from rest_framework import serializers
from .models import User, SelectedBook, SubscribeAuthor, Comment
from library.serializers import BookSerializer, AuthorSerializer
from library.models import Book, Author
from .validators import validate_user_password, validate_email


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


class AddPointsSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)
    points = serializers.IntegerField(min_value=1, max_value=100)
