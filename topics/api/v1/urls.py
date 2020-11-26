"""
API V1: Topics Urls
"""
###
# Libraries
###
from django.conf.urls import url, include
from rest_framework_nested import routers

from .views import (
    ListCreateTopicViewSet,
    UpdateDeleteTopicView
)

###
# Routers
###
""" Main router """
router = routers.SimpleRouter()

router.register('topics', ListCreateTopicViewSet, basename='topics')
router.register('topics', UpdateDeleteTopicView, basename='topics')
###
# URLs
###
urlpatterns = [
    url(r'^', include(router.urls)),
]
