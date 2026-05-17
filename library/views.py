from django.shortcuts import render
from rest_framework import viewsets
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from .models import Author, Book
from .serializers import AuthorSerializer, BookSerializer
from .filters import BookFilter
from .paginators import ListPagination
from users.permissions import IsModeratorOrReadOnly


class AuthorViewSet(viewsets.ModelViewSet):
    queryset = Author.objects.all()
    serializer_class = AuthorSerializer
    pagination_class = ListPagination

    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            permission_classes = [IsModeratorOrReadOnly]
        else:
            permission_classes = [IsAuthenticated]

        return [permission() for permission in permission_classes]


class BookViewSet(viewsets.ModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = BookFilter
    pagination_class = ListPagination

    def get_permissions(self):
        """
        Разные права для разных действий
        """
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            # Создание/изменение/удаление только модераторам
            permission_classes = [IsModeratorOrReadOnly]
        elif self.action == 'list':
            # Список книг могут видеть все аутентифицированные
            permission_classes = [IsAuthenticated]
        else:
            # Детали книги могут видеть все аутентифицированные
            permission_classes = [IsAuthenticated]

        return [permission() for permission in permission_classes]

    def get_queryset(self):
        """Базовый queryset для всех"""
        return Book.objects.select_related('author').prefetch_related('comment_set').all()


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def upload_book_text(request, book_id):
    """
    Загрузка текста книги (только для авторизованных)
    """
    try:
        book = get_object_or_404(Book, id=book_id)

        # Проверяем, есть ли файл в запросе
        if 'text_file' not in request.FILES:
            return Response(
                {'error': 'Файл не выбран'},
                status=status.HTTP_400_BAD_REQUEST
            )

        file = request.FILES['text_file']

        # Сохраняем файл
        book.text_file = file
        book.save()

        # Возвращаем обновленную информацию о книге
        serializer = BookSerializer(book, context={'request': request})
        return Response({
            'success': True,
            'message': 'Текст успешно загружен',
            'book': serializer.data
        }, status=status.HTTP_200_OK)

    except Exception as e:
        return Response(
            {'error': str(e)},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


@api_view(['GET'])
@permission_classes([])  # Доступно всем
def download_book_text(request, book_id):
    """
    Скачивание текста книги
    """
    from django.http import FileResponse
    import os

    book = get_object_or_404(Book, id=book_id)

    if not book.has_text():
        return Response(
            {'error': 'Текст для этой книги не загружен'},
            status=status.HTTP_404_NOT_FOUND
        )

    # Увеличиваем счетчик скачиваний
    book.increment_download_count()

    # Отправляем файл
    response = FileResponse(
        book.text_file,
        as_attachment=True,  # Скачивается как файл
        filename=f"{book.title}_{book.author.name}{book.get_file_extension()}"
    )

    # Защита от XSS
    response['X-Content-Type-Options'] = 'nosniff'
    return response


@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_book_text(request, book_id):
    """
    Удаление текста книги (только для авторов/админов)
    """
    book = get_object_or_404(Book, id=book_id)

    # Проверка прав (только автор или админ)
    if not request.user.is_staff and request.user != book.author:
        return Response(
            {'error': 'Недостаточно прав'},
            status=status.HTTP_403_FORBIDDEN
        )

    if book.text_file:
        # Удаляем файл с диска
        book.text_file.delete(save=False)
        book.text_file = None
        book.save()

        return Response({
            'success': True,
            'message': 'Текст удален'
        })

    return Response(
        {'error': 'Текст не найден'},
        status=status.HTTP_404_NOT_FOUND
    )
