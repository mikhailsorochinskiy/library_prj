from rest_framework import status
from rest_framework import viewsets
from rest_framework.views import APIView
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes, action
from .models import User, SubscribeAuthor, SelectedBook, Comment, ScoreLog
from .serializers import UserSerializer, CommentSerializer, AddPointsSerializer
from rest_framework.permissions import AllowAny, IsAuthenticated
from library.models import Author, Book
from .services import UserService


class UserViewSet(viewsets.ModelViewSet):
    serializer_class = UserSerializer
    queryset = User.objects.all()

    def get_permissions(self):
        if self.action in ['create', 'login']:
            return [AllowAny()]
        return [IsAuthenticated()]

    def perform_create(self, serializer):
        user = serializer.save()
        user.set_password(user.password)
        user.save()

    @action(detail=False, methods=['get'])
    def me(self, request):
        """Текущий пользователь"""
        serializer = self.get_serializer(request.user)
        return Response(serializer.data)


class SubscribeAuthorApiView(APIView):
    def post(self, *args, **kwargs):
        user = self.request.user
        author_id = self.request.data.get('author')
        author_item = get_object_or_404(Author, id=author_id)

        sub_item = SubscribeAuthor.objects.filter(user=user, author=author_item)

        if sub_item.exists():
            sub_item.delete()
            message = 'Подписка удалена'
        else:
            SubscribeAuthor.objects.create(user=user, author=author_item)
            message = 'Подписка добавлена'
            subscribe_before = ScoreLog.objects.filter(user=user, author=author_item)
            if not subscribe_before.exists():
                UserService.add_points(user.email, 2)
                ScoreLog.objects.create(user=user, author=author_item, points=2)
        return Response({"message": message})


class SelectedBookApiView(APIView):
    def post(self, *args, **kwargs):
        user = self.request.user
        book_id = self.request.data.get('book')
        book_item = get_object_or_404(Book, id=book_id)

        selected_item = SelectedBook.objects.filter(user=user, book=book_item)

        if selected_item.exists():
            selected_item.delete()
            message = 'Книга удалена из избранных'
        else:
            SelectedBook.objects.create(user=user, book=book_item)
            message = 'Книга добавлена в избранное'
            selected_book_before = ScoreLog.objects.filter(user=user, book=book_item, comment=False)
            if not selected_book_before.exists():
                UserService.add_points(user.email, 1)
                ScoreLog.objects.create(user=user, book=book_item, points=1)
        return Response({"message": message})


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    queryset = Comment.objects.all()

    def perform_create(self, serializer):
        comment = serializer.save()
        comment.owner = self.request.user
        comment.save()

        owner = self.request.user
        comments = ScoreLog.objects.filter(book=comment.book, user=owner, comment=True)
        if len(comments) < 3:
            UserService.add_points(owner.email, 5)
            ScoreLog.objects.create(book=comment.book, user=owner, points=5, comment=True)


@api_view(['POST'])
@permission_classes([AllowAny])  # Или [IsAuthenticated] если нужна аутентификация
def add_test_points(request):
    """
        API endpoint для добавления баллов за прохождение теста
        Пример запроса:
        POST /api/add-test-points/
        {
            "user_id": 1,
            "points": 10
        }
    """
    serializer = AddPointsSerializer(data=request.data)
    if not serializer.is_valid():
        return Response(
            {'success': False, 'errors': serializer.errors},
            status=status.HTTP_400_BAD_REQUEST
        )

    email = serializer.validated_data['email']
    points = serializer.validated_data.get('points')

    try:
        user = User.objects.get(email=email)
        if user.is_tested:
            return Response({
                'success': True,
                'message': 'Пользователь с данным email уже прошел тест.',
            }, status=status.HTTP_200_OK)
        else:
            result = UserService.add_points(email, points)
            if result['success']:
                return Response({
                    'success': True,
                    'message': result['message'],
                    'data': {
                        'user': result.get('user'),
                        'points_added': result['points_added'],
                        'total_points': result['total_points']
                    }
                }, status=status.HTTP_200_OK)

            else:
                return Response({
                    'success': False,
                    'message': result['message']
                }, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        return Response({
            'success': False,
            'message': f'Пользователь с данным email не найден. {e}'
        })
