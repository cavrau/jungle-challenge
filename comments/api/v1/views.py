"""
API V1: Comments Views
"""
###
# Libraries
###

from rest_framework import permissions, exceptions

from . import serializers
from comments.models import Comment
from posts.models import Post
from helpers.views import ListCreateViewSet, UpdateDeleteViewSet
from helpers.permissions import IsOwnerOrReadOnly


###
# Viewsets
###


class ListCreateCommentViewSet(ListCreateViewSet):
    serializer_class = serializers.CommentSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)

    def get_queryset(self):
        return Comment.objects.filter(post__topic__url_name=self.kwargs['topic_pk'], post__id=self.kwargs['post_pk'])

    def create(self, req, topic_pk, post_pk):
        if(not Post.objects.filter(id=post_pk, topic__url_name=topic_pk).exists()):
            raise exceptions.NotFound('Post not found')
        req.data['post'] = post_pk
        return super(ListCreateCommentViewSet, self).create(req)


class UpdateDeleteCommentViewSet(UpdateDeleteViewSet):
    lookup_field = 'pk'
    serializer_class = serializers.CommentSerializer
    permission_classes = (IsOwnerOrReadOnly,)

    def get_queryset(self):

        return Comment.objects.filter(post__topic__url_name=self.kwargs['topic_pk'], post__id=self.kwargs['post_pk'])

    def update(self, req, topic_pk, post_pk, pk):

        req.data['id'] = pk
        req.data['post'] = post_pk
        return super(UpdateDeleteCommentViewSet, self).update(req)
