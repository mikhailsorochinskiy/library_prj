from django.urls import path
from rest_framework.routers import DefaultRouter
from .views import AuthorViewSet, BookViewSet, upload_book_text, download_book_text, delete_book_text

app_name = 'library'

router = DefaultRouter()
router.register(r'authors', AuthorViewSet, basename='authors')
router.register(r'books', BookViewSet, basename='books')


urlpatterns = [
    path('books/<int:book_id>/upload-text/', upload_book_text,
       name='upload-book-text'),
    path('books/<int:book_id>/download/', download_book_text,
       name='download-book-text'),
    path('books/<int:book_id>/delete-text/', delete_book_text,
       name='delete-book-text'),
] + router.urls
