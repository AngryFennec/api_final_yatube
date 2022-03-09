from django.shortcuts import get_object_or_404
from rest_framework.permissions import (
    IsAuthenticated,
    IsAuthenticatedOrReadOnly
)
from rest_framework.mixins import ListModelMixin, CreateModelMixin
from rest_framework import filters, viewsets
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.exceptions import ValidationError

from posts.models import Post, Group, Follow

from .serializers import (
    PostSerializer,
    GroupSerializer,
    CommentSerializer,
    FollowSerializer
)
from .permissions import IsAuthorOrSafe


class PostViewSet(viewsets.ModelViewSet):
    """Вьюсет для запросов, касающихся постов."""
    queryset = Post.objects.all()
    permission_classes = [IsAuthorOrSafe]
    serializer_class = PostSerializer

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class GroupViewSet(viewsets.ReadOnlyModelViewSet):
    """Вьюсет для запросов, касающихся групп."""
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]


class CommentViewSet(viewsets.ModelViewSet):
    """Вьюсет для запросов, касающихся комментариев."""
    serializer_class = CommentSerializer
    permission_classes = [IsAuthorOrSafe]

    def perform_create(self, serializer):
        post_id = self.kwargs.get('post_id')
        post = get_object_or_404(Post, pk=post_id)
        serializer.save(author=self.request.user, post=post)

    def get_queryset(self):
        post = get_object_or_404(Post, pk=self.kwargs.get('post_id'))
        return post.comments.all()


class FollowViewSet(viewsets.GenericViewSet, ListModelMixin, CreateModelMixin):
    """Вьюсет для запросов, касающихся фолловинга."""
    queryset = Follow.objects.all()
    serializer_class = FollowSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    search_fields = ('user__username', 'following__username')

    def get_queryset(self):
        user = self.request.user
        return Follow.objects.filter(user=user)

    def perform_create(self, serializer):
        if self.request.user.username == self.request.data['following']:
            raise ValidationError('Нельзя подписаться на себя')
        serializer.save(user=self.request.user)
