from rest_framework import viewsets, permissions
from rest_framework.response import Response

from api.comment.permissions import IsOwnerOrAdminOrReadOnly
from api.comment.serializers import CommentCreateSerializer
from common.comment.models import Comment


class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentCreateSerializer
    lookup_field = 'guid'
    permission_classes = [permissions.IsAuthenticated, IsOwnerOrAdminOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data)
