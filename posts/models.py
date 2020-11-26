from django.db import models
from helpers.models import TimestampModel, NotNullNotBlankCharField
from topics.models import Topic
from accounts.models import User

# Create your models here.


class Post(TimestampModel, models.Model):
    title = NotNullNotBlankCharField(max_length=50)
    content = NotNullNotBlankCharField(max_length=400)
    topic = models.ForeignKey(Topic, on_delete=models.CASCADE)
    author = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        unique_together = ['title', 'topic']
        ordering = ['-created_at']
