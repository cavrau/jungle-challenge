"""
Comment admin
"""
###
# Libraries
###
from django.contrib import admin

from . import models


###
# Inline Admin Models
###


###
# Main Admin Models
###
@admin.register(models.Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'content', 'get_post', 'get_topic', 'author', 'created_at', 'updated_at')

    def get_topic(self, obj):
        return obj.post.topic.url_name

    def get_post(self, obj):
        return obj.post.title
