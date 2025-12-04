from rest_framework import serializers
from .models import User, SelectedBook, SubscribeAuthor


class UserSerializer(serializers.ModelSerializer):
    selected_books = serializers.SerializerMethodField()

    def get_selected_books(self, obj):
        user = self.context.get("request").user
        if not user:
            return False
        selected_books = SelectedBook.objects.filter(user=user)
        result = []
        for selected_book in selected_books:
            result.append(selected_book.book.title)
        return result

    class Meta:
        model = User
        fields = ('id', 'email', 'avatar', 'points', 'selected_books')
