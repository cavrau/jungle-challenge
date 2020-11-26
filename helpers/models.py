"""
Model helper
"""
###
# Libraries
###
from django.db import models
from django.utils import timezone


class NotNullNotBlankCharField(models.CharField):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs, null=False, blank=False)

###
# Helpers
###


class TimestampModel(models.Model):
    '''
        Extend this model if you wish to have automatically updated
        created_at and updated_at fields.
    '''

    class Meta:
        abstract = True

    created_at = models.DateTimeField(null=False, blank=True)
    updated_at = models.DateTimeField(null=False, blank=True)

    def save(self, *args, **kwargs):
        if not self.id:
            self.created_at = timezone.now()
        self.updated_at = timezone.now()
        return super(TimestampModel, self).save(*args, **kwargs)
