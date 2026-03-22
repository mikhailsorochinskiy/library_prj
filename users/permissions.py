# users/permissions.py
from rest_framework import permissions


class IsModeratorOrReadOnly(permissions.BasePermission):
    """
    Разрешает чтение всем аутентифицированным,
    изменение только модераторам и админам
    """

    def has_permission(self, request, view):
        # Чтение разрешено всем аутентифицированным
        if request.method in permissions.SAFE_METHODS:
            return request.user.is_authenticated

        # Запись только модераторам и админам
        return request.user.is_authenticated and (
                request.user.is_staff or
                request.user.groups.filter(name='Moderators').exists()
        )


class IsModerator(permissions.BasePermission):
    """
    Доступ только для модераторов и админов
    """

    def has_permission(self, request, view):
        return request.user.is_authenticated and (
                request.user.is_staff or
                request.user.groups.filter(name='Moderators').exists()
        )


class IsOwnerOrReadOnly(permissions.BasePermission):
    """
    Разрешает редактирование только владельцу объекта
    (для комментариев, избранного)
    """

    def has_object_permission(self, request, view, obj):
        # Чтение разрешено всем
        if request.method in permissions.SAFE_METHODS:
            return True

        # Запись только владельцу или модератору/админу
        return (
                obj.user == request.user or
                request.user.is_staff or
                request.user.groups.filter(name='Moderators').exists()
        )


class IsAdminOrModerator(permissions.BasePermission):
    """
    Доступ только для админов и модераторов
    """

    def has_permission(self, request, view):
        return request.user.is_authenticated and (
                request.user.is_staff or
                request.user.groups.filter(name='Moderators').exists()
        )
