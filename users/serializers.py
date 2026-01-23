from rest_framework import serializers
from .models import User, SelectedBook, SubscribeAuthor, Comment
from library.serializers import BookSerializer, AuthorSerializer
from library.models import Book, Author


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

    selected_books = SelectedBookSerializer(many=True, read_only=True)
    subscribes = SubscribeAuthorSerializer(many=True, read_only=True)

    class Meta:
        model = User
        fields = ('id', 'email', 'avatar', 'points', 'selected_books', 'subscribes')


class CommentSerializer(serializers.ModelSerializer):

    class Meta:
        model = Comment
        fields = ('id', 'owner', 'book', 'text')
