from django.db import models

from apps.common.models import TimeStampedModel
from apps.user.models import User


class Post(TimeStampedModel):
    title = models.CharField(max_length=200)
    content = models.TextField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    likes = models.ManyToManyField(User, related_name='likes', blank=True)
    hits = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.title

    def like_nums(self):
        return len(self.likes.all())


class Hashtag(models.Model):
    name = models.CharField(max_length=60, unique=True)

    def __str__(self):
        return self.name


class PostHashtag(models.Model):
    post = models.ForeignKey(Post, related_name='hashtags', on_delete=models.CASCADE)
    hashtag = models.ForeignKey(Hashtag, related_name='posts', on_delete=models.CASCADE)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['post', 'hashtag'], name='post_hashtag_constraint')
        ]
