from django_filters import rest_framework as filters
from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework.permissions import SAFE_METHODS
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from apps.post.models import Post
from .filters import PostFilter
from .paginations import PostPagination
from .permissions import PostPermission
from .serializers import PostSerializer, PostCreateUpdateSerializer


class PostViewSet(ModelViewSet):
    """ 게시물 CRUD ViewSet """
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [PostPermission]
    filter_backends = [filters.DjangoFilterBackend, OrderingFilter, SearchFilter]
    ordering_fields = ['created_at', 'like_nums', 'hits']
    ordering = ['created_at']
    search_fields = ['title', 'content', 'user__email']
    filterset_class = PostFilter
    pagination_class = PostPagination

    def get_serializer_class(self):
        if self.request.method in SAFE_METHODS:
            return PostSerializer
        else:
            return PostCreateUpdateSerializer

    def retrieve(self, request, *args, **kwargs):
        """ 게시물 retrieve할 때마다 조회수 1 증가 """
        instance = self.get_object()
        instance.hits += 1  # 조회수 1 증가
        instance.save()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)
