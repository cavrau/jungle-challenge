from django.db import models
from helpers.models import TimestampModel
from accounts.models import User
from helpers.models import NotNullNotBlankCharField


class Topic(TimestampModel, models.Model):
    name = NotNullNotBlankCharField(max_length=50)
    title = NotNullNotBlankCharField(max_length=30)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    description = NotNullNotBlankCharField(max_length=200)
    url_name = models.SlugField(max_length=30, unique=True, blank=False, null=False)

    class Meta:
        ordering = ['-created_at']
