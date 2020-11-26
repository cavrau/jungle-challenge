"""
API V1: Posts Serializers
"""
###
# Libraries
###
from accounts.models import User
from rest_framework import serializers

from posts.models import Post
from comments.models import Comment


###
# Serializers
###
class CommentSerializer(serializers.ModelSerializer):
    author = serializers.PrimaryKeyRelatedField(required=False, queryset=User.objects.all())
    post = serializers.PrimaryKeyRelatedField(required=False, queryset=Post.objects.all())

    class Meta:
        model = Comment
        fields = '__all__'
