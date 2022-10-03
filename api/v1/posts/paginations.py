from rest_framework.pagination import PageNumberPagination


class PostPagination(PageNumberPagination):
    default_limit = 10
