from .models import Author, Book
from rest_framework import serializers
from users.models import Comment



class BookSerializer(serializers.ModelSerializer):
    comments = serializers.SerializerMethodField()

    def get_comments(self, obj):
        from users.serializers import CommentSerializer
        comments = obj.comment_set.all()
        return CommentSerializer(comments, many=True).data

    class Meta:
        model = Book
        fields = ('id', 'title', 'author', 'description', 'preview_image', 'genre', 'disposition', 'comments')


class AuthorSerializer(serializers.ModelSerializer):
    books = BookSerializer(source='book_set', many=True, read_only=True)

    class Meta:
        model = Author
        fields = ('id', 'name', 'bio', 'photo', 'books')
