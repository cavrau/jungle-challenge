"""
API V1: Posts Urls
"""
###
# Libraries
###
from django.conf.urls import url, include
from rest_framework_nested import routers

from posts.api.v1.urls import posts_router
from .views import (
    ListCreateCommentViewSet,
    UpdateDeleteCommentViewSet
)


###
# Routers
###

comments_router = routers.NestedSimpleRouter(posts_router, r'posts', lookup='post')
comments_router.register(r'comments', ListCreateCommentViewSet, basename='comments')
comments_router.register(r'comments', UpdateDeleteCommentViewSet, basename='comments')
###
# URLs
###
urlpatterns = [
    url(r'^', include(comments_router.urls)),
]
