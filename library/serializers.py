from .models import Author, Book
from rest_framework import serializers


class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = '__all__'


class AuthorSerializer(serializers.ModelSerializer):
    books = BookSerializer(source='books', many=True, read_only=True)

    class Meta:
        model = Author
        fields = ('name', 'bio', 'photo', 'books')
