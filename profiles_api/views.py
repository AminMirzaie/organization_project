from django.shortcuts import render
from . import models,serializers
from rest_framework import viewsets, filters
from rest_framework.authentication import TokenAuthentication
from . import permissions
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.settings import api_settings
# Create your views here.

class UserProfileViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.UserProfileSerializer
    queryset = models.UserProfile.objects.all()
    authentication_classes = (TokenAuthentication,)
    permission_classes = (permissions.UpdateOwnProfile,)
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name','email')


class UserLoginApi(ObtainAuthToken):
    renderer_classes = api_settings.DEFAULT_RENDERER_CLASSES
