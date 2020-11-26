"""
API V1: Posts Views
"""
###
# Libraries
###

from posts.models import Post
from rest_framework import permissions
from helpers.views import ListCreateViewSet, UpdateDeleteViewSet

from . import serializers
from helpers.permissions import IsOwnerOrReadOnly


###
# Viewsets
###


class ListCreatePostViewSet(ListCreateViewSet):
    serializer_class = serializers.PostSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)

    def get_queryset(self):
        return Post.objects.filter(topic__url_name=self.kwargs['topic_pk'])

    def create(self, req, topic_pk):
        req.data['topic'] = topic_pk
        return super(ListCreatePostViewSet, self).create(req)


class UpdateDeletePostViewSet(UpdateDeleteViewSet):
    lookup_field = 'pk'
    serializer_class = serializers.PostSerializer
    permission_classes = (IsOwnerOrReadOnly,)

    def get_queryset(self):
        return Post.objects.filter(topic__url_name=self.kwargs['topic_pk'])

    def update(self, req, topic_pk, pk):
        req.data['id'] = pk
        req.data['topic'] = topic_pk
        return super(UpdateDeletePostViewSet, self).update(req)
