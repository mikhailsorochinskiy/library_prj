from .models import Author, Book
from rest_framework import serializers
from users.models import Comment



class BookSerializer(serializers.ModelSerializer):
    comments = serializers.SerializerMethodField()
    text_file_url = serializers.SerializerMethodField()
    file_size = serializers.SerializerMethodField()
    file_extension = serializers.SerializerMethodField()
    has_text = serializers.BooleanField(read_only=True)

    def get_comments(self, obj):
        from users.serializers import CommentSerializer
        comments = obj.comment_set.all()
        return CommentSerializer(comments, many=True).data

    def get_text_file_url(self, obj):
        """URL для скачивания/просмотра"""
        return obj.get_text_url()

    def get_file_size(self, obj):
        """Размер файла"""
        return obj.get_file_size()

    def get_file_extension(self, obj):
        """Расширение файла"""
        return obj.get_file_extension()

    class Meta:
        model = Book
        fields = ('id', 'title', 'author', 'description', 'preview_image', 'genre', 'disposition',
                  'comments', 'text_file', 'text_file_url', 'file_size', 'file_extension', 'has_text')
        extra_kwargs = {
            'text_file': {'write_only': True},  # Не показываем путь в файловой системе
        }


class AuthorSerializer(serializers.ModelSerializer):
    books = BookSerializer(source='book_set', many=True, read_only=True)

    class Meta:
        model = Author
        fields = ('id', 'name', 'bio', 'photo', 'books')
