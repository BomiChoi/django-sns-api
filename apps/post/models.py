from django.db import models

from apps.common.models import TimeStampedModel
from apps.user.models import User


class Post(TimeStampedModel):
    title = models.CharField(max_length=200)
    content = models.TextField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    hashtags = models.ManyToManyField('Hashtag', related_name='products', blank=True)
    likes = models.ManyToManyField(User, related_name='likes', blank=True)
    hits = models.PositiveIntegerField(default=0)


class Hashtag(models.Model):
    name = models.CharField(max_length=60, unique=True)
