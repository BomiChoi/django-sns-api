from django.db import transaction
from rest_framework import serializers
from rest_framework.exceptions import NotAuthenticated

from apps.post.models import Post, Hashtag, PostHashtag


class PostHashtagSerializer(serializers.ModelSerializer):
    """ 해시태그 시리얼라이저 """
    hashtag = serializers.CharField(read_only=True, source='hashtag.name')

    class Meta:
        model = PostHashtag
        fields = ('id', 'hashtag')


class PostSerializer(serializers.ModelSerializer):
    """ 게시물 조회 시리얼라이저 """
    hits = serializers.IntegerField(read_only=True)
    user = serializers.PrimaryKeyRelatedField(read_only=True)
    hashtags = PostHashtagSerializer(many=True, read_only=True)
    likes = serializers.PrimaryKeyRelatedField(many=True, read_only=True)
    like_nums = serializers.IntegerField(read_only=True)
    is_liked = serializers.SerializerMethodField()
    created_at = serializers.DateTimeField(read_only=True)
    updated_at = serializers.DateTimeField(read_only=True)

    class Meta:
        model = Post
        fields = (
            'id',
            'title',
            'content',
            'user',
            'hashtags',
            'likes',
            'like_nums',
            'is_liked',
            'hits',
            'created_at',
            'updated_at',
        )

    def get_is_liked(self, obj):
        """ 현재 요청한 사용자가 해당 게시물에 좋아요를 눌렀는지 여부 반환 """
        return self.context['request'].user in obj.likes.all()


class PostCreateUpdateSerializer(serializers.Serializer):
    """ 게시물 생성/수정 시리얼라이저 """
    title = serializers.CharField(max_length=200)
    content = serializers.CharField()
    hashtags_txt = serializers.CharField(write_only=True, required=False, allow_null=True)
    hashtags = PostHashtagSerializer(many=True, read_only=True)

    def validate(self, attrs):
        # 현재 요청한 유저 정보 가져오기
        user = self.context['request'].user
        if not user.is_authenticated:
            raise NotAuthenticated(detail='로그인하지 않은 사용자입니다.')
        attrs['user'] = user
        return attrs

    def add_hashtags(self, post, hashtags_txt):
        if hashtags_txt:
            hashtags = hashtags_txt.split(',')
            for h in hashtags:
                # 샵과 양 끝 공백 제거
                name = h.replace('#', '').trim()
                # 띄어쓰기 _로 대체
                name = name.replace(' ', '_')
                
                hashtag, created = Hashtag.objects.get_or_create(name=name)
                if hashtag not in post.hashtags.all():
                    PostHashtag.objects.create(post=post, hashtag=hashtag)

    @transaction.atomic()
    def create(self, validated_data):
        # 해시태그 텍스트 추출
        hashtags_txt = None
        if 'hashtags_txt' in validated_data:
            hashtags_txt = validated_data.pop('hashtags_txt')

        # 게시물 생성
        post = Post.objects.create(**validated_data)

        # 해시태그 추가
        if hashtags_txt:
            self.add_hashtags(post, hashtags_txt)

        return post

    @transaction.atomic()
    def update(self, instance, validated_data):
        # 게시물 수정
        title = validated_data.get('title', None)
        if title:
            instance.title = title
        content = validated_data.get('content', None)
        if content:
            instance.content = content
        instance.save()

        # 해시태그 모두 삭제 후 다시 추가
        if 'hashtags_txt' in validated_data:
            hashtags_txt = validated_data.pop('hashtags_txt')
            instance.hashtags.all().delete()
            self.add_hashtags(instance, hashtags_txt)

        return instance
