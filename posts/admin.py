"""
Post admin
"""
###
# Libraries
###
from django.contrib import admin

from . import models
from comments.models import Comment

###
# Inline Admin Models
###


class CommentInline(admin.TabularInline):
    model = Comment
    extra = 1


###
# Main Admin Models
###
@admin.register(models.Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'content', 'get_topic', 'author', 'created_at', 'updated_at')
    inlines = [CommentInline]

    def get_topic(self, obj):
        return obj.topic.url_name
