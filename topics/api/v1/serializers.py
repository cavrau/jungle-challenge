"""
API V1: Topics Serializers
"""
###
# Libraries
###
from accounts.models import User
from rest_framework import serializers

from topics.models import Topic


###
# Serializers
###
class TopicSerializer(serializers.ModelSerializer):
    author = serializers.PrimaryKeyRelatedField(required=False, queryset=User.objects.all())

    class Meta:
        model = Topic
        fields = '__all__'
