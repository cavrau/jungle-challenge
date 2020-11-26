"""
Topics URL Configuration
"""
###
# Libraries
###
from django.conf.urls import url, include

urlpatterns = [
    url(r'^api/v1/', include('topics.api.v1.urls'))
]
