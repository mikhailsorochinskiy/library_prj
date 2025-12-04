from django.urls import path
from rest_framework.routers import DefaultRouter
from .views import UserViewSet, SelectedBookApiView, SubscribeAuthorApiView
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

app_name = 'users'

router = DefaultRouter()
router.register(r'users', UserViewSet, basename='users')


urlpatterns = [
    path('login/', TokenObtainPairView.as_view(), name='login'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('subscribes/', SubscribeAuthorApiView.as_view(), name='subscribe_author'),
    path('selected-book/', SelectedBookApiView.as_view(), name='selected_book'),
] + router.urls
