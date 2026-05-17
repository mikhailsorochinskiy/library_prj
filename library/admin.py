from django.contrib import admin
from .models import Author, Book
from users.models import Comment


class CommentInline(admin.TabularInline):
    model = Comment
    extra = 0
    readonly_fields = ('owner', 'text')


@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    search_fields = ('name',)


@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'author', 'genre', 'disposition', 'has_text')
    list_display_links = ('id', 'title')
    search_fields = ('title', 'author__name')
    list_filter = ('genre', 'disposition', 'created_at')
    list_select_related = ('author',)
    autocomplete_fields = ('author',)
    inlines = [CommentInline]
