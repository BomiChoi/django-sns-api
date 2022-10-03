from rest_framework.exceptions import NotAuthenticated
from rest_framework.generics import CreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.response import Response

from .serializers import UserCreateSerializer, UserDetailSerializer


class UserCreateView(CreateAPIView):
    """ 회원가입 뷰 """

    serializer_class = UserCreateSerializer


class UserDetailView(RetrieveUpdateDestroyAPIView):
    """ 회원정보 조회 / 회원정보 수정 / 회원탈퇴 뷰 """

    serializer_class = UserDetailSerializer

    def get_object(self):
        """ 현재 요청한 사용자 반환"""
        if not self.request.user.is_authenticated:
            raise NotAuthenticated(detail='로그인하지 않은 사용자입니다.')
        return self.request.user

    def destroy(self, request, *args, **kwargs):
        """개인정보 삭제 후 비활성화"""
        user = self.get_object()
        user.name = None
        user.gender = None
        user.age = None
        user.phone = None
        user.is_active = False
        user.save()
        return Response(status=204)
