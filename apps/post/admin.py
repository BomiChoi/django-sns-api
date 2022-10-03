from django.contrib import admin

from .models import Post, Hashtag


# Register your models here.

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'title',
        'content',
        'user',
        'created_at',
        'updated_at',
        'hits'
    )


@admin.register(Hashtag)
class HashtagAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'name'
    )
