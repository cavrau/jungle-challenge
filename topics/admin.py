"""
Topic admin
"""
###
# Libraries
###
from django.contrib import admin

from . import models
from posts.models import Post


###
# Inline Admin Models
###
class PostInline(admin.StackedInline):
    model = Post
    extra = 1


###
# Main Admin Models
###
@admin.register(models.Topic)
class TopicAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'name', 'author', 'description', 'url_name', 'created_at', 'updated_at',)
    inlines = [PostInline]
