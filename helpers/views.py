'''
Views helper
'''
###
# Libraries
###
from rest_framework import (
    mixins,
    viewsets
)

###
# Viewsets
###


class ListCreateViewSet(mixins.ListModelMixin, mixins.CreateModelMixin, viewsets.GenericViewSet):
    def create(self, req):
        req.data['author'] = req.user.id
        return super(ListCreateViewSet, self).create(req)


class UpdateDeleteViewSet(
    mixins.RetrieveModelMixin,
    mixins.DestroyModelMixin,
    mixins.UpdateModelMixin,
    viewsets.GenericViewSet
):
    def update(self, req, *args, **kwargs):
        req.data['author'] = req.user.id
        return super(UpdateDeleteViewSet, self).update(req, *args, **kwargs)
