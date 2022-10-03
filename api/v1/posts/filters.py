from django_filters import rest_framework as filters

from apps.post.models import Post


class PostFilter(filters.FilterSet):
    class Meta:
        model = Post
        fields = ['title', 'content', 'user']
