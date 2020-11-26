"""
API V1: Topics Views
"""
###
# Libraries
###

from topics.models import Topic
from rest_framework import permissions, exceptions
from helpers.views import ListCreateViewSet, UpdateDeleteViewSet

from . import serializers
from helpers.permissions import IsOwnerOrReadOnly


###
# Viewsets
###


class ListCreateTopicViewSet(ListCreateViewSet):
    queryset = Topic.objects.all()
    serializer_class = serializers.TopicSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)


class UpdateDeleteTopicView(UpdateDeleteViewSet):
    lookup_field = 'url_name'
    queryset = Topic.objects.all()
    serializer_class = serializers.TopicSerializer
    permission_classes = (IsOwnerOrReadOnly,)

    def update(self, req, url_name):
        if 'url_name' in req.data.keys():
            if url_name != req.data['url_name']:
                raise exceptions.ParseError('Url_name of topic can\'t be changed')
        req.data['url_name'] = url_name
        return super(UpdateDeleteTopicView, self).update(req)
