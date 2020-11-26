"""
Accounts URL Configuration
"""
###
# Libraries
###
from django.conf.urls import url, include

urlpatterns = [
    url(r'^api/v1/', include('posts.api.v1.urls'))
]
