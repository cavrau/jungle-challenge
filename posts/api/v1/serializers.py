"""
API V1: Posts Serializers
"""
###
# Libraries
###
from accounts.models import User
from rest_framework import serializers

from topics.models import Topic
from posts.models import Post


###
# Serializers
###
class PostSerializer(serializers.ModelSerializer):
    author = serializers.PrimaryKeyRelatedField(required=False, queryset=User.objects.all())
    topic = serializers.SlugRelatedField(queryset=Topic.objects.all(), slug_field='url_name')

    class Meta:
        model = Post
        fields = '__all__'
