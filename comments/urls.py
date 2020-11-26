"""
Comments URL Configuration
"""
###
# Libraries
###
from django.conf.urls import url, include

urlpatterns = [
    url(r'^api/v1/', include('comments.api.v1.urls'))
]
