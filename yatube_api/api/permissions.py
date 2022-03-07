from rest_framework.permissions import BasePermission, SAFE_METHODS


class IsAuthorOrSafe(BasePermission):
    """
    Проверка на автора - только он может изменять объекты
     либо safe methods для остальных
     """

    def has_object_permission(self, request, view, obj):
        return (request.method in SAFE_METHODS
                or obj.author == request.user
                )