"""
API V1: Posts Urls
"""
###
# Libraries
###
from django.conf.urls import url, include
from rest_framework_nested import routers

from topics.api.v1.urls import router
from .views import (
    ListCreatePostViewSet,
    UpdateDeletePostViewSet
)


###
# Routers
###

posts_router = routers.NestedSimpleRouter(router, r'topics', lookup='topic')
posts_router.register(r'posts', ListCreatePostViewSet, basename='posts')
posts_router.register(r'posts', UpdateDeletePostViewSet, basename='posts')
###
# URLs
###
urlpatterns = [
    url(r'^', include(posts_router.urls)),
]
