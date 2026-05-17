from django.contrib import admin
from .models import User, Comment, SelectedBook, SubscribeAuthor, ScoreLog


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('id', 'email', 'points', 'is_tested', 'is_active', 'is_staff')
    list_display_links = ('id', 'email')
    search_fields = ('email',)
    list_filter = ('is_tested', 'is_active', 'is_staff', 'groups')


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('id', 'owner', 'book')


@admin.register(SelectedBook)
class SelectedBookAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'book')


@admin.register(SubscribeAuthor)
class SubscribeAuthorAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'author')


@admin.register(ScoreLog)
class ScoreLogAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'author', 'book', 'comment', 'points')
