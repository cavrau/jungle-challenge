from django.db import models

from helpers.models import TimestampModel, NotNullNotBlankCharField
from accounts.models import User
from posts.models import Post
# Create your models here.


class Comment(TimestampModel):
    title = NotNullNotBlankCharField(max_length=50)
    content = models.TextField(max_length=500, null=False, blank=False)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    author = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        ordering = ['-created_at']
