from django.contrib import admin

from .models import Post, Hashtag, PostHashtag


# Register your models here.

class PostHashtagInline(admin.TabularInline):
    model = PostHashtag


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'title',
        'content',
        'user',
        'like_nums',
        'hits',
        'created_at',
        'updated_at',
    )
    inlines = (PostHashtagInline,)


@admin.register(Hashtag)
class HashtagAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'name'
    )
