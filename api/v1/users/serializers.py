from django.contrib.auth.hashers import make_password, check_password
from django.db import transaction
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from apps.user.models import User, GENDER_CHOICES


class UserCreateSerializer(serializers.Serializer):
    """ 회원가입 시리얼라이저 """

    id = serializers.IntegerField(read_only=True)
    email = serializers.EmailField(max_length=255)
    password = serializers.CharField(min_length=6, max_length=128, style={'input_type': 'password'})
    name = serializers.CharField(max_length=30, required=False, allow_null=True)
    gender = serializers.ChoiceField(choices=GENDER_CHOICES, required=False, allow_null=True)
    age = serializers.IntegerField(required=False, allow_null=True)

    @transaction.atomic()
    def create(self, validated_data):
        """ 신규가입 / 재가입 """

        # 기존 유저 불러오거나 신규 유저 생성
        user, created = User.objects.get_or_create(email=validated_data['email'], defaults={
            'password': make_password(None)
        })
        print(user, created)

        # 재가입일 경우 이전 비밀번호와 일치하는지 확인 후 활성화
        password = validated_data['password']
        if not created:
            if not check_password(password, user.password):
                raise ValidationError({'password': '비밀번호가 일치하지 않습니다. 알맞은 비밀번호를 입력하거나 다른 이메일을 사용하세요.'})
            user.is_active = True
        else:
            user.set_password(password)

        # 유저 정보 업데이트
        user.name = validated_data.get('name', None)
        user.gender = validated_data.get('gender', None)
        user.age = validated_data.get('age', None)
        user.phone = validated_data.get('phone', None)

        # 인스턴스 저장 후 반환
        user.save()
        return user


class UserSerializer(serializers.ModelSerializer):
    """ 유저 기본 시리얼라이저 """

    is_staff = serializers.BooleanField(read_only=True)
    is_superuser = serializers.BooleanField(read_only=True)
    is_active = serializers.BooleanField(read_only=True)

    class Meta:
        model = User
        fields = (
            'id',
            'email',
            'name',
            'gender',
            'age',
            'phone',
            'is_staff',
            'is_superuser',
            'is_active',
            'created_at',
            'updated_at',
        )


class UserDetailSerializer(UserSerializer):
    """ 유저 상세정보 시리얼라이저 """

    email = serializers.EmailField(read_only=True)

    def update(self, instance, validated_data):
        """ 유저 정보 업데이트 후 반환 """
        
        # 유저 정보 업데이트
        name = validated_data.get('name', None)
        if name:
            instance.name = name
        gender = validated_data.get('gender', None)
        if gender:
            instance.gender = gender
        age = validated_data.get('age', None)
        if age:
            instance.age = age
        phone = validated_data.get('phone', None)
        if phone:
            instance.phone = phone

        # 인스턴스 저장 후 반환
        instance.save()
        return instance
